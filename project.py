
from task import Task

class Project:
    """Represents a project that contains multiple tasks."""

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
        print(f"[SUCCESS] Task '{task.title}' added to project '{self.name}'.")

    def delete_task(self, task_title: str) -> None:
        for task in self.tasks:
            if task.title == task_title:
                self.tasks.remove(task)
                print(f"[SUCCESS] Task '{task_title}' deleted from project '{self.name}'.")
                return
        print("[ERROR] Task not found.")

    def get_task(self, task_title: str) -> Task | None:
        for task in self.tasks:
            if task.title == task_title:
                return task
        return None

    def show_tasks(self) -> None:
        if not self.tasks:
            print(f"No tasks in project '{self.name}'.")
        else:
            print(f"\nTasks in project '{self.name}':")
            for t in self.tasks:
                print(f"  - {t}")

    def edit(self, new_name: str | None = None, new_description: str | None = None) -> bool:
        updated = False
        if new_name:
            if len(new_name) > 30:
                print("[ERROR] Project name must be <= 30 characters.")
                return False
            self.name = new_name.strip()
            updated = True
        if new_description:
            if len(new_description) > 150:
                print("[ERROR] Project description must be <= 150 characters.")
                return False
            self.description = new_description.strip()
            updated = True
        if not updated:
            print("[INFO] Nothing to update.")
            return False
        print("[SUCCESS] Project updated successfully.")
        return True

    def __str__(self) -> str:
        output = f"Project: {self.name}\nDescription: {self.description}"
        if not self.tasks:
            output += "\n(No tasks yet)"
        else:
            output += "\nTasks:"
            for task in self.tasks:
                output += f"\n  - {task}"
        return output
