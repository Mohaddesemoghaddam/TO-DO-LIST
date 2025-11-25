
import os
from dotenv import load_dotenv
from project import Project
from task import Task

load_dotenv()

class Manager:
    """Handles CRUD operations and validation for Projects and Tasks (In-Memory)."""

    def __init__(self) -> None:
        self.projects: list[Project] = []
        self.max_projects: int = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))
        self.max_tasks: int = int(os.getenv("MAX_NUMBER_OF_TASK", 20))

    def add_project(self, name: str, description: str = "") -> None:
        if any(p.name.lower() == name.lower() for p in self.projects):
            print("[ERROR] Project name already exists.")
            return
        if len(name) > 30 or len(description) > 150:
            print("[ERROR] Name must be ≤30 chars and description ≤150 chars.")
            return
        if len(self.projects) >= self.max_projects:
            print("[ERROR] Maximum number of projects reached.")
            return

        project = Project(name.strip(), description.strip())
        self.projects.append(project)
        print(f"[SUCCESS] Project '{name}' created successfully.")

    def show_all_projects(self) -> None:
        if not self.projects:
            print("No projects found.")
            return
        print("\n=== Projects ===")
        for p in self.projects:
            print(p)
            print("-" * 30)

    def find_project(self, name: str) -> Project | None:
        for project in self.projects:
            if project.name.lower() == name.lower():
                return project
        print("[ERROR] Project not found.")
        return None

    def delete_project(self, name: str) -> None:
        before = len(self.projects)
        self.projects = [p for p in self.projects if p.name.lower() != name.lower()]
        if len(self.projects) < before:
            print(f"[SUCCESS] Project '{name}' deleted successfully.")
        else:
            print("[ERROR] Project not found.")

    def edit_project(self, name: str, new_name: str | None = None, new_description: str | None = None) -> None:
        project = self.find_project(name)
        if not project:
            return
        if new_name and any(p.name.lower() == new_name.lower() for p in self.projects if p != project):
            print("[ERROR] Another project already has this name.")
            return
        project.edit(new_name, new_description)

    def add_task_to_project(self, project_name: str, title: str, description: str, deadline: str) -> None:
        project = self.find_project(project_name)
        if not project:
            return
        if len(project.tasks) >= self.max_tasks:
            print("[ERROR] Maximum number of tasks reached.")
            return
        task = Task(title, description, deadline)
        project.add_task(task)
        print(f"[SUCCESS] Task '{title}' added to project '{project_name}'.")

    def update_task_status(self, project_name: str, task_title: str, new_status: str) -> None:
        project = self.find_project(project_name)
        if not project:
            return
        task = project.get_task(task_title)
        if not task:
            print("[ERROR] Task not found.")
            return
        if not task._validate_status(new_status):
            print("[ERROR] Invalid status.")
            return
        task.status = new_status
        print(f"[SUCCESS] Task '{task_title}' status updated to '{new_status}'.")

    def delete_task_from_project(self, project_name: str, task_title: str) -> None:
        project = self.find_project(project_name)
        if not project:
            return
        project.delete_task(task_title)

    def edit_task(
        self,
        project_name: str,
        task_title: str,
        new_title: str | None = None,
        new_description: str | None = None,
        new_deadline: str | None = None,
        new_status: str | None = None,
    ) -> None:
        project = self.find_project(project_name)
        if not project:
            return
        task = project.get_task(task_title)
        if not task:
            print("[ERROR] Task not found.")
            return
        task.edit(new_title, new_description, new_deadline, new_status)

    def show_tasks_of_project(self, project_name: str) -> None:
        project = self.get_project_by_id(project_name)
        if not project:
            print("[ERROR] Project not found.")
            return
        if not project.tasks:
            print("[INFO] No tasks found for this project.")
            return

        print(f"\nTasks for project: {project.name}")
        print("-" * 40)
        for i, task in enumerate(project.tasks, start=1):
            print(f"Task #{i}")
            print(f"Title: {task.title}")
            print(f"Status: {task.status}")
            print(f"Deadline: {task.deadline or 'N/A'}")
            print("-" * 40)

    def get_project_by_id(self, project_identifier: str) -> Project | None:
        for project in self.projects:
            if str(project.name) == str(project_identifier):
                return project
        return None

