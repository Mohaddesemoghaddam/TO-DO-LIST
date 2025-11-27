from typing import Optional, ClassVar
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.base import Base


class Task(Base):
    """ORM Model that represents tasks stored in PostgreSQL."""
    __tablename__ = "tasks"

    # فیلدِ وضعیت‌های مجاز (همون Validation قدیمی)
    VALID_STATUSES: ClassVar[tuple[str, ...]] = ("todo", "doing", "done")

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255))
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(30), default="todo")

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), nullable=False)
    project: Mapped["Project"] = relationship("Project", back_populates="tasks")

    # -------------------------------
    # VALIDATION METHODS (اختیاری برای CLI)
    # -------------------------------
    def _validate_title(self, title: str) -> str:
        title = title.strip()
        if len(title) < 3 or len(title) > 30:
            raise ValueError("[ERROR] Task title must be 3–30 characters.")
        return title

    def _validate_description(self, description: str) -> str:
        description = description.strip()
        if len(description) < 3 or len(description) > 150:
            raise ValueError("[ERROR] Task description must be 3–150 characters.")
        return description

    def _validate_deadline(self, deadline_str: str) -> datetime:
        try:
            return datetime.strptime(deadline_str, "%Y-%m-%d")
        except ValueError:
            raise ValueError("[ERROR] Invalid date format. Use YYYY‑MM‑DD.")

    def _validate_status(self, status: str) -> str:
        status = status.lower().strip()
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(f"[ERROR] Invalid status! Choose one of: {valid}")
        return status

    # -------------------------------
    # EDIT / UPDATE FEATURE
    # -------------------------------
    def edit(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        deadline: Optional[str] = None,
        status: Optional[str] = None,
    ) -> bool:
        updated = False

        if title:
            self.title = self._validate_title(title)
            updated = True
        if description:
            self.description = self._validate_description(description)
            updated = True
        if deadline:
            self.deadline = self._validate_deadline(deadline)
            updated = True
        if status:
            self.status = self._validate_status(status)
            updated = True

        return updated

    # -------------------------------
    # STRING REPRESENTATION
    # -------------------------------
    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
