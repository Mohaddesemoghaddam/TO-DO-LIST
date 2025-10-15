# task.py

from datetime import datetime

class Task:
    """
    Represents a single task within a project.
    """

    VALID_STATUSES = ["TODO", "IN_PROGRESS", "DONE"]

    def __init__(self, task_id: int, title: str, description: str, deadline: str, status: str = "TODO"):
        # --- Initialization with validations ---
        if len(title) > 30:
            raise ValueError("Task title must be 30 characters or fewer.")
        if len(description) > 150:
            raise ValueError("Task description must be 150 characters or fewer.")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Invalid status. Choose from {self.VALID_STATUSES}.")
        try:
            datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be in YYYY-MM-DD format.")

        self.id = task_id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status

    def update(self, title=None, description=None, deadline=None, status=None):
        """
        Update task fields with validation.
        """
        if title:
            if len(title) > 30:
                raise ValueError("Task title must be ≤ 30 characters.")
            self.title = title

        if description:
            if len(description) > 150:
                raise ValueError("Task description must be ≤ 150 characters.")
            self.description = description

        if deadline:
            datetime.strptime(deadline, "%Y-%m-%d")
            self.deadline = deadline

        if status:
            if status not in self.VALID_STATUSES:
                raise ValueError(f"Invalid status: {status}")
            self.status = status

    def __str__(self):
        return f"[{self.id}] {self.title} ({self.status}) - due {self.deadline}"
