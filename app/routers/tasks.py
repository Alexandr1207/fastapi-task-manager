import datetime
import uuid

from fastapi import APIRouter, Query, Path, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from schemas.tasks import TaskResponse, TaskStatus, TaskCreate, TaskPriority, TaskCreatedResponse, TaskUpdate
from storage.memory import tasks


router = APIRouter(prefix='/tasks', tags=['Tasks'])


def pagination(limit: int = Query(10), offset: int = Query(0)):
    return {'limit': limit, 'offset': offset}


@router.get('/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Get task by id')
async def get_task_by_id(task_id: Annotated[int, Path(gt=0)]):
    for task in tasks:
        if task['id'] == task_id:
            return task 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.get('/', 
            response_model=list[TaskResponse], 
            status_code=status.HTTP_200_OK, 
            summary='Get tasks'
            )
async def get_tasks(
    status: Annotated[TaskStatus | None, Query()] = None, 
    search: Annotated[str | None, Query()] = None,
    priority: Annotated[TaskPriority | None, Query()] = None,
    page: Annotated[pagination, Depends()] = None
    ):
    tsk = tasks
    if status:
        tsk = list(filter(lambda x: x['status'] == status, tsk))
    if search:
        tsk = list(filter(lambda x: search.lower() in x['title'].lower(), tsk))
    if priority:
        tsk = list(filter(lambda x: x['priority'] == priority, tsk))
    return tsk


@router.post('/', response_model=TaskCreatedResponse, status_code=status.HTTP_201_CREATED, summary='Create new task')
async def create_task(task: Annotated[TaskCreate, Body()]):
    task_dict = task.model_dump(exclude_unset=True)
    task_dict.update({
        'id': len(tasks) + 1,
        'uuid': uuid.uuid4(),
        'created_at': datetime.date.today(),
        'updated_at': datetime.date.today()
    })
    tasks.append(task_dict)
    message = 'Task created successfully'
    task_dict = TaskResponse(**task_dict)
    return {'message': message, 'task': task_dict}
    


@router.patch(
        '/{task_id}', 
        response_model=TaskResponse, 
        status_code=status.HTTP_200_OK,
        summary='Update task'
        )
async def update_task(task_id: Annotated[int, Path(gt=0)], task: Annotated[TaskUpdate, Body()]):
    task_dict = task.model_dump(exclude_unset=True)
    task_dict.update({'updated_at': datetime.date.today()})
    for i in range(len(tasks)):
        if tasks[i]['id'] == task_id:
            stored_item_data = tasks[i]
            stored_item_model = TaskResponse(**stored_item_data)
            updated_item = stored_item_model.model_copy(update=task_dict)
            tasks[i] = jsonable_encoder(updated_item)
            return tasks[i]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")


@router.delete('/{task_id}', status_code=status.HTTP_200_OK, summary='Delete task')
async def delete_task(task_id: Annotated[int, Path(gt=0)]):
    for i in range(len(tasks)):
        if tasks[i]['id'] == task_id:
            tasks.pop(i)
            return {'message': 'Task deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")