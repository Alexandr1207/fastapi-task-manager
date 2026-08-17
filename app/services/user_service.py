from sqlalchemy import select

from app.core.security import hash_password
from app.database.models import User
from sqlalchemy.orm import Session

from app.schemas.users import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return db.scalars(stmt).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalars(stmt).first()


def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    new_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user