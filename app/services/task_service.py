from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from database.models import Task
from schemas.tasks import TaskCreate, TaskUpdate



def add_task(db: Session, task_dict: TaskCreate, user_id: int) -> Task | None:
    new_task = Task(**task_dict.model_dump(), user_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def read_tasks(db: Session, search: str = None, priority: str = None, status: str = None, user_id: int = None) -> list[Task] | None:
    conditions = [Task.user_id == user_id]
    if search:
        conditions.append(Task.title.ilike(f"%{search}%"))
    if priority:
        conditions.append(Task.priority == priority)
    if status:
        conditions.append(Task.status == status)
    stmt = select(Task).where(*conditions)        
    task = db.scalars(stmt).all()
    return task


def read_task_by_id(db: Session, task_id: int, user_id: int) -> Task | None:
    stmt = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return db.scalars(stmt).first()


def update_task_db(db: Session, task_id: int, updated_item: TaskUpdate, user_id: int) -> Task | None:
    stmt = update(Task).where(Task.id == task_id, Task.user_id == user_id).values(**updated_item.model_dump(exclude_unset=True))
    db.execute(stmt)
    db.commit()
    new_task = read_task_by_id(db, task_id=task_id, user_id=user_id)
    if new_task:
        db.refresh(new_task)
    return new_task


def delete_task_db(db: Session, task_id: int, user_id: int):
    stmt = delete(Task).where(Task.id == task_id, Task.user_id == user_id)
    db.execute(stmt)
    db.commit()


def get_all(db: Session):
    stmt = select(Task)
    return db.scalars(stmt).all()
