from sqlalchemy import select

from app.database.models import User
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalars(stmt).first()


def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user