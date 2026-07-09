from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Category, Task


def get_categories_db(db: Session):
    return db.scalars(select(Category)).all()


def get_category_by_id_db(db: Session, cat_id: int):
    stmt = select(Category).where(Category.id == cat_id)
    return db.scalars(stmt).first()


def get_category_by_name_db(db: Session, cat_name: str):
    stmt = select(Category).where(Category.name == cat_name)
    return db.scalars(stmt).first()


def create_category_db(db: Session, category: dict):
    new_cat = Category(**category)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


def update_category_db(db: Session, cat_id: int, cat_dict: dict):
    stmt = update(Category).where(Category.id == cat_id).values(**cat_dict)
    db.execute(stmt)
    db.commit()
    new_cat = get_category_by_id_db(db, cat_id)
    return new_cat


def delete_category_db(db: Session, cat_id: int):
    stmt = delete(Category).where(Category.id == cat_id)
    db.execute(stmt)
    db.commit()