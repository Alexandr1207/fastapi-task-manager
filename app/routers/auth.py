from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy.orm import Session
from database.database import get_db 

from services.user_service import get_user_by_username, get_user_by_email
from core.security import create_access_token, verify_password

from schemas.users import TokenResponse, LoginRequest


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=login.email)
    if not user or not verify_password(password=login.password, hashed_password=user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not acitve")
    token_data = {
        "sub": str(user.id),
        "role": user.role.value
    }
    access_token = create_access_token(token_data)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }