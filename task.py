
from datetime import datetime
from typing import ClassVar



class Task:
    """Represents a single task with validation logic."""
    VALID_STATUSES: ClassVar[tuple[str, ...]] = ("todo", "doing", "done")

    def __init__(
        self,
        title: str,
        description: str,
        deadline: str,
        status: str = "todo",
    ) -> None:
        self.title: str = self._validate_title(title)
        self.description: str = self._validate_description(description)
        self.deadline: str = self._validate_deadline(deadline)
        self.status: str = self._validate_status(status)

    # -------------------------------
    # VALIDATION METHODS
    # -------------------------------
    def _validate_title(self, title: str) -> str:
        title = title.strip()
        if len(title) < 3 or len(title) > 30:
            print("[ERROR] Task title must be 3–30 characters.")
            raise ValueError()
        return title

    def _validate_description(self, description: str) -> str:
        description = description.strip()
        if len(description) < 3 or len(description) > 150:
            print("[ERROR] Task description must be 3–150 characters.")
            raise ValueError()
        return description

    def _validate_deadline(self, deadline_str: str) -> str:
        """Check date format YYYY-MM-DD."""
        try:
            datetime.strptime(deadline_str, "%Y-%m-%d")
            return deadline_str
        except ValueError:
            print("[ERROR] Invalid date format. Use YYYY‑MM‑DD.")
            raise

    def _validate_status(self, status: str) -> str:
        status = status.lower().strip()
        if status not in self.VALID_STATUSES:
            valid = ", ".join(self.VALID_STATUSES)
            print(f"[ERROR] Invalid status! Choose one of: {valid}")
            raise ValueError()
        return status

    # -------------------------------
    # EDIT FEATURE (Phase 2)
    # -------------------------------
    def edit(
        self,
        title: str | None = None,
        description: str | None = None,
        deadline: str | None = None,
        status: str | None = None,
    ) -> bool:
        """Edit any task property with validation."""
        updated: bool = False

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

        if not updated:
            print("[INFO] Nothing to update.")
            return False

        print("[SUCCESS] Task updated successfully.")
        return True

    # -------------------------------
    # STRING REPRESENTATION
    # -------------------------------
    def __str__(self) -> str:
        return f"{self.title} | {self.status} | {self.deadline}"

