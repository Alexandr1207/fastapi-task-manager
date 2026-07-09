from fastapi import Depends
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session

from database.models import Task


def add_task(db: Session, task_dict: dict):
    new_task = Task(**task_dict)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def read_tasks(db: Session, search: str = None, priority: str = None, status: str = None):
    conditions = []
    if search:
        conditions.append(Task.title.ilike(f"%{search}%"))
    if priority:
        conditions.append(Task.priority == priority)
    if status:
        conditions.append(Task.status == status)
    stmt = select(Task).where(*conditions)        
    task = db.scalars(stmt).all()
    return task


def read_task_by_id(db: Session, task_id: int):
    stmt = select(Task).where(Task.id == task_id)
    return db.scalars(stmt).first()


def update_task_db(db: Session, task_id: int, updated_item: dict):
    stmt = update(Task).where(Task.id == task_id).values(**updated_item)
    db.execute(stmt)
    db.commit()
    new_task = read_task_by_id(db, task_id=task_id)
    db.refresh(new_task)
    return new_task


def delete_task_db(db: Session, task_id: int):
    stmt = delete(Task).where(Task.id == task_id)
    db.execute(stmt)
    db.commit()


def category_has_tasks(db: Session, cat_id: int):
    stmt = select(Task).where(Task.category_id == cat_id)
    return db.scalars(stmt).first() is not None