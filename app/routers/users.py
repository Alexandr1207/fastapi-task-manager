from typing import Annotated

from fastapi import APIRouter, Body, HTTPException,status, Depends

from sqlalchemy.orm import Session

from schemas.users import UserCreate, UserResponse
from services.user_service import get_user_by_email, get_user_by_username, create_user
from database.database import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse , status_code=status.HTTP_201_CREATED)
def user_create(user: Annotated[UserCreate, Body()], db: Session = Depends(get_db)):
    if get_user_by_email(db=db, email=user.email):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email is already in use")
    if get_user_by_username(db=db, username=user.username):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username is already in use")
    new_user = create_user(db=db, user=user)
    return new_user