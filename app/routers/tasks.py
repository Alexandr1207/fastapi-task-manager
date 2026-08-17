import datetime
import uuid

from fastapi import APIRouter, Query, Path, Body, status, HTTPException, Depends
from typing import Annotated

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.database.models import User
from app.routers.auth import get_current_user
from app.services.category_service import get_category_by_id_db
from app.schemas.tasks import TaskResponse, TaskStatus, TaskCreate, TaskPriority, TaskCreatedResponse, TaskUpdate
from app.services.task_service import add_task, read_tasks, read_task_by_id, update_task_db, delete_task_db, get_all
from app.database.database import get_db


router = APIRouter(prefix='/tasks', tags=['Tasks'])


def require_admin(current_user: User = Depends(get_current_user)):
    if not current_user.role == UserRole.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not admin")



def pagination(limit: int = Query(10), offset: int = Query(0)):
    return {'limit': limit, 'offset': offset}


@router.get("/all", response_model=list[TaskResponse])
async def get_all_tasks(db: Session = Depends(get_db), is_admin: User = Depends(require_admin)):
    return get_all(db=db)


@router.get('/{task_id}', response_model=TaskResponse, status_code=status.HTTP_200_OK, summary='Get task by id')
async def get_task_by_id(task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = read_task_by_id(db, task_id=task_id, user_id=current_user.id)
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
    ):
    tsk = read_tasks(db, search=search, priority=priority, status=status, user_id=current_user.id)
    return tsk[pagination['offset']: pagination['offset'] + pagination['limit']]


@router.post('/', response_model=TaskCreatedResponse, status_code=status.HTTP_201_CREATED, summary='Create new task')
async def create_task(task: Annotated[TaskCreate, Body()], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = get_category_by_id_db(db=db, cat_id=task.category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    created_task = add_task(db, task, current_user.id)
    message = 'Task created successfully'
    return {'message': message, 'task': created_task}
    


@router.patch(
        '/{task_id}', 
        response_model=TaskResponse, 
        status_code=status.HTTP_200_OK,
        summary='Update task'
        )
async def update_task(
    task_id: Annotated[int, Path(gt=0)], 
    task: Annotated[TaskUpdate, Body()], 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    task = update_task_db(db=db, task_id=task_id, updated_item=task, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete('/{task_id}', status_code=status.HTTP_200_OK, summary='Delete task')
async def delete_task(task_id: Annotated[int, Path(gt=0)], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = read_task_by_id(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    delete_task_db(db=db, task_id=task_id, user_id=current_user.id)
    return {'message': 'Task deleted successfully'}


