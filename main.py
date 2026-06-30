import datetime
import uuid

from fastapi import FastAPI, Depends, Query, Path, Body, status
from typing import Annotated

from schemas import TaskResponse, TaskStatus, TaskCreate, TaskPriority, TaskCreated, TaskCreatedResponse

app = FastAPI()


tasks = []


@app.get('/tasks/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: Annotated[int, Path(gt=0)]):
    for task in tasks:
        if task['id'] == task_id:
            return task 
    return {"error": "task not found"}


@app.get('/tasks', response_model=list[TaskResponse], status_code=status.HTTP_200_OK)
async def get_tasks(
    status: Annotated[TaskStatus | None, Query()] = None, 
    search: Annotated[str | None, Query()] = None,
    priority: Annotated[TaskPriority | None, Query()] = None
    ):
    tsk = tasks
    if status:
        tsk = list(filter(lambda x: x['status'] == status, tsk))
    if search:
        tsk = list(filter(lambda x: search.lower() in x['title'].lower(), tsk))
    if priority:
        tsk = list(filter(lambda x: priority in x['priority'], tsk))
    return tsk


@app.post('/tasks', response_model=TaskCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task: Annotated[TaskCreate, Body()]):
    task_dict = task.model_dump()
    task_dict.update({
        'id': len(tasks) + 1,
        'uuid': uuid.uuid4(),
        'created_at': datetime.date.today(),
        'updated_ at': datetime.date.today()
    })
    tasks.append(task_dict)
    message = 'Task created successfully'
    task_dict = TaskCreated(**task_dict)
    return {'message': message, 'task': task_dict}
    


@app.patch('/tasks/{task_id}', response_model=TaskResponse, response_model_exclude_unset=True, status_code=status.HTTP_200_OK)
async def update_task(task_id: Annotated[int, Path(gt=0)], task: Annotated[TaskCreate, Body()]):
    task_dict = task.model_dump()
    task_dict.update({'updated_at': datetime.date.today()})
    for i in range(len(tasks)):
        if tasks[i]['id'] == task_id:
            tasks[i].update(task_dict)
            return tasks[i]
    return {'error': 'task not found'}


@app.delete('/tasks/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task(task_id: Annotated[int, Path(gt=0)]):
    for i in range(len(tasks)):
        if tasks[i]['id'] == task_id:
            tasks.pop(i)
            return {'message': 'Task deleted successfully'}
    return {'message': 'Task not found'}