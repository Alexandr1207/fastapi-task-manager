from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from database.models import Category
from schemas.tasks import CategoryCreate


def get_categories_db(db: Session) -> list[Category] | None:
    return db.scalars(select(Category)).all()


def get_category_by_id_db(db: Session, cat_id: int) -> Category | None:
    stmt = select(Category).where(Category.id == cat_id)
    return db.scalars(stmt).first()


def get_category_by_name_db(db: Session, cat_name: str) -> Category | None:
    stmt = select(Category).where(Category.name == cat_name)
    return db.scalars(stmt).first()


def create_category_db(db: Session, category: CategoryCreate) -> Category | None:
    new_cat = Category(**category.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat


def update_category_db(db: Session, cat_id: int, cat_dict: CategoryCreate) -> Category | None:
    stmt = update(Category).where(Category.id == cat_id).values(**cat_dict.model_dump(exclude_unset=True))
    db.execute(stmt)
    db.commit()
    new_cat = get_category_by_id_db(db, cat_id)
    return new_cat


def delete_category_db(db: Session, cat_id: int):
    stmt = delete(Category).where(Category.id == cat_id)
    db.execute(stmt)
    db.commit()