from sqlalchemy import String, Uuid, Enum, Date, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import uuid 
import datetime
from database.database import Base
from schemas.tasks import TaskStatus, TaskPriority


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True),
        default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(50))
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus))
    priority: Mapped[TaskPriority] = mapped_column(Enum(TaskPriority))
    deadline: Mapped[Optional[datetime.date]] = mapped_column(Date)
    created_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    updated_at: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today, onupdate=datetime.date.today)

    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="tasks")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(30))

    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")


