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


class SubTask(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    done: bool = False


class Category(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=20)


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    description: str = Field(min_length=3, max_length=50)
    status: TaskStatus
    priority: TaskPriority
    deadline: datetime.date | None = None


class TaskResponse(TaskCreate):
    uuid: uuid.UUID
    created_at: datetime.date
    updated_at: datetime.date


class TaskCreatedResponse(BaseModel):
    message: str = 'Task created successfully'
    task: TaskResponse


class TaskUpdate(BaseModel):
    title: str | None = Field(min_length=3, max_length=30, default=None)
    description: str | None = Field(min_length=3, max_length=50, default=None)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    deadline: datetime.date | None = None