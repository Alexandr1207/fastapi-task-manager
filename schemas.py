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
    category: Category
    tags: set[str] = Field(default_factory=set)
    subtasks: list[SubTask] = Field(default_factory=list)
    deadline: datetime.date | None = None


class TaskResponse(TaskCreate):
    id: int = Field(gt=0)
    uuid: uuid.UUID
    created_at: datetime.date
    updated_at: datetime.date


class TaskCreated(BaseModel):
    title: str = Field(min_length=3, max_length=30)
    status: TaskStatus
    priority: TaskPriority
    deadline: datetime.date | None = None


class TaskCreatedResponse(BaseModel):
    message: str = 'Task created successfully'
    task: TaskCreated