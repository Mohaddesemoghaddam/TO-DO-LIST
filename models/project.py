from typing import List, Optional
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base  # ← کلاس Base از db/base.py
from models.task import Task  # ← مدل Task که جدول مربوطش هست


class Project(Base):
    """Database model that represents a Project."""
    __tablename__ = "projects"

    # ستون‌ها
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))

    # رابطه با Task
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="project")

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}')>"
