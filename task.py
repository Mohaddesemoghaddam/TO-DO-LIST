# task.py
from datetime import datetime

class Task:
    """Represents a single task with basic validation."""
    VALID_STATUSES = ("todo", "doing", "done")

    def __init__(self, title, description, deadline, status="todo"):
        self.title = self._validate_title(title)
        self.description = description.strip()
        self.deadline = self._validate_deadline(deadline)
        self.status = self._validate_status(status)

    def _validate_title(self, title: str):
        if not title or len(title.strip()) < 3:
            raise ValueError("[ERROR] Task title must be at least 3 characters.")
        return title.strip()

    def _validate_deadline(self, deadline_str: str):
        """Check date format YYYY-MM-DD."""
        try:
            datetime.strptime(deadline_str, "%Y-%m-%d")
            return deadline_str
        except ValueError:
            raise ValueError("[ERROR] Invalid date format. Use YYYY-MM-DD.")

    def _validate_status(self, status: str):
        status = status.lower()
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            raise ValueError(f"[ERROR] Invalid status! Choose one of: {valid}")
        return status

    def __str__(self):
        return f"{self.title} | {self.status} | {self.deadline}"
