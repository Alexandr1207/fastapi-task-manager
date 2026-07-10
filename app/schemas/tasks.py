import datetime
import uuid
from pydantic import BaseModel, Field
from enum import Enum


class TaskStatus(str, Enum):
    open = 'open'
    close = 'close'


class TaskPriority(str, Enum):
    low = 'low'
    high = 'high'


class CategoryCreate(BaseModel):
    name: str = Field(min_length=3, max_length=20)


class CategoryResponse(CategoryCreate):
    id: int


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=50)
    status: TaskStatus
    priority: TaskPriority
    deadline: datetime.date | None = None

    category_id: int | None = Field(gt=0)


class TaskResponse(TaskCreate):
    uuid: uuid.UUID
    created_at: datetime.date
    updated_at: datetime.date

    category: CategoryCreate | None


class TaskCreatedResponse(BaseModel):
    message: str = 'Task created successfully'
    task: TaskResponse


class TaskUpdate(BaseModel):
    title: str | None = Field(min_length=3, max_length=30, default=None)
    description: str | None = Field(min_length=3, max_length=50, default=None)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime.date | None = None
    category_id: int | None = None