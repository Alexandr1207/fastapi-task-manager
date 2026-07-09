import datetime
import uuid

from fastapi import APIRouter, Query, Path, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from sqlalchemy.orm import Session

from services.category_service import get_category_by_id_db
from schemas.tasks import TaskResponse, TaskStatus, TaskCreate, TaskPriority, TaskCreatedResponse, TaskUpdate
from services.task_service import add_task, read_tasks, read_task_by_id, update_task_db, delete_task_db
from database.database import get_db


router = APIRouter(prefix='/tasks', tags=['Tasks'])


def pagination(limit: int = Query(10), offset: int = Query(0)):
    return {'limit': limit, 'offset': offset}


@router.get('/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Get task by id')
async def get_task_by_id(task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    task = read_task_by_id(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.get('/',
            response_model=list[TaskResponse],
            status_code=status.HTTP_200_OK,
            summary='Get tasks'
            )
async def get_tasks(
    status: Annotated[TaskStatus | None, Query()] = None, 
    search: Annotated[str | None, Query()] = None,
    priority: Annotated[TaskPriority | None, Query()] = None,
    pagination: Annotated[pagination, Depends()] = None,
    db: Session = Depends(get_db)
    ):
    tsk = read_tasks(db, search=search, priority=priority, status=status)
    return tsk[pagination['offset']: pagination['offset'] + pagination['limit']]


@router.post('/', response_model=TaskCreatedResponse, status_code=status.HTTP_201_CREATED, summary='Create new task')
async def create_task(task: Annotated[TaskCreate, Body()], db: Session = Depends(get_db)):
    task_dict = task.model_dump(exclude_unset=True)
    category = get_category_by_id_db(db=db, cat_id=task_dict['category_id'])
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    created_task = add_task(db, task_dict)
    message = 'Task created successfully'
    return {'message': message, 'task': created_task}
    


@router.patch(
        '/{task_id}', 
        response_model=TaskResponse, 
        status_code=status.HTTP_200_OK,
        summary='Update task'
        )
async def update_task(task_id: Annotated[int, Path(gt=0)], task: Annotated[TaskUpdate, Body()], db: Session = Depends(get_db)):
    task_dict = task.model_dump(exclude_unset=True)
    task = update_task_db(db=db, task_id=task_id, updated_item=task_dict)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete('/{task_id}', status_code=status.HTTP_200_OK, summary='Delete task')
async def delete_task(task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db)):
    task = read_task_by_id(db=db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    delete_task_db(db=db, task_id=task_id)
    return {'message': 'Task deleted successfully'}