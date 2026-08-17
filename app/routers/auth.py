from fastapi import APIRouter, Depends, status, HTTPException

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session
from app.database.models import User
from app.database.database import get_db 

from app.services.user_service import get_user_by_email, get_user_by_id
from app.core.security import ALGORITHM, SECRET_KEY, create_access_token, verify_password

from app.schemas.users import TokenResponse, LoginRequest


router = APIRouter(prefix="/auth", tags=["auth"])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = int(decoded_token["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user = get_user_by_id(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


@router.post("/login", response_model=TokenResponse)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db=db, email=form_data.username)
    if not user or not verify_password(password=form_data.password, hashed_password=user.hashed_password):
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


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


