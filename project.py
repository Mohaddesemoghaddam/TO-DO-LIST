# project.py
from task import Task

class Project:
    """Holds multiple tasks and enforces validation rules."""

    def __init__(self, name):
        self.name = self._validate_name(name)
        self.tasks = []

    def _validate_name(self, name):
        if not name or len(name.strip()) < 3:
            raise ValueError("[ERROR] Project name must be at least 3 characters.")
        return name.strip()

    def add_task(self, task: Task, max_tasks: int):
        if len(self.tasks) >= max_tasks:
            raise ValueError("[ERROR] Task limit reached for this project.")
        if any(t.title.lower() == task.title.lower() for t in self.tasks):
            raise ValueError("[ERROR] Task title already exists in this project.")
        self.tasks.append(task)

    def remove_task(self, title: str):
        self.tasks = [t for t in self.tasks if t.title.lower() != title.lower()]

    def get_task(self, title: str):
        for t in self.tasks:
            if t.title.lower() == title.lower():
                return t
        raise ValueError("[ERROR] Task not found.")

    def __str__(self):
        result = f"\n📁 Project: {self.name}\n"
        if not self.tasks:
            result += "  (No tasks yet)\n"
        else:
            for t in self.tasks:
                result += f"  - {t}\n"
        return result
