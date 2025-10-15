# project.py

from task import Task

class Project:
    """
    Represents a project containing multiple tasks.
    """

    def __init__(self, project_id: int, name: str, description: str):
        if len(name) > 30:
            raise ValueError("Project name must be 30 characters or fewer.")
        if len(description) > 150:
            raise ValueError("Project description must be 150 characters or fewer.")

        self.id = project_id
        self.name = name
        self.description = description
        self.tasks: list[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def remove_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def list_tasks(self):
        return [str(task) for task in self.tasks]

    def __str__(self):
        return f"[{self.id}] {self.name} - {len(self.tasks)} tasks"
