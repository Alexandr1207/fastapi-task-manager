from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, EmailStr

from core.enums import UserRole


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True
    )


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None