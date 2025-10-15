# project.py
from task import Task

class Project:
    """Represents a project that contains multiple tasks."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.tasks = []

    # -------------------------------
    # CRUD METHODS FOR TASKS
    # -------------------------------
    def add_task(self, task: Task):
        """Add a Task object to this project."""
        self.tasks.append(task)
        print(f"[SUCCESS] Task '{task.title}' added to project '{self.name}'.")

    def delete_task(self, task_title: str):
        """Delete a task by its title."""
        for task in self.tasks:
            if task.title == task_title:
                self.tasks.remove(task)
                print(f"[SUCCESS] Task '{task_title}' deleted from project '{self.name}'.")
                return
        print("[ERROR] Task not found.")

    def get_task(self, task_title: str):
        """Find and return a task object by its title, or None if not found."""
        for task in self.tasks:
            if task.title == task_title:
                return task
        return None

    def show_tasks(self):
        """Display all tasks in this project."""
        if not self.tasks:
            print(f"No tasks in project '{self.name}'.")
        else:
            print(f"\nTasks in project '{self.name}':")
            for t in self.tasks:
                print(f"  - {t}")

    # -------------------------------
    # EDIT FEATURE (Phase 2)
    # -------------------------------
    def edit(self, new_name=None, new_description=None):
        """
        Edit project name/description with validation.
        The duplicate name validation occurs in Manager.
        """
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

    # -------------------------------
    # OUTPUT STRING (for CLI display)
    # -------------------------------
    def __str__(self):
        """String representation for printing project details."""
        output = f"Project: {self.name}\nDescription: {self.description}"
        if not self.tasks:
            output += "\n(No tasks yet)"
        else:
            output += "\nTasks:"
            for task in self.tasks:
                output += f"\n  - {task}"
        return output
