from sqlalchemy import String, Uuid, Enum, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
import uuid 
import datetime
from database.database import Base
from schemas.tasks import TaskStatus, TaskPriority


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(50))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus))
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority))
    deadline: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[datetime.date] = mapped_column(Date)
    updated_at: Mapped[datetime.date] = mapped_column(Date)


print("MODELS LOADED FROM:", __file__)
