# manager.py
import os
from dotenv import load_dotenv
from project import Project
from task import Task

load_dotenv()

class Manager:
    """Handles CRUD operations and validation for Projects and Tasks (In-Memory)."""

    def __init__(self):
        self.projects = []
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", 20))

    # -------------------------------
    # PROJECT METHODS
    # -------------------------------
    def add_project(self, name, description=""):
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

    def show_all_projects(self):
        if not self.projects:
            print("No projects found.")
            return
        print("\n=== Projects ===")
        for p in self.projects:
            print(p)
            print("-" * 30)

    def find_project(self, name):
        for project in self.projects:
            if project.name.lower() == name.lower():
                return project
        print("[ERROR] Project not found.")
        return None

    def delete_project(self, name):
        before = len(self.projects)
        self.projects = [p for p in self.projects if p.name.lower() != name.lower()]
        if len(self.projects) < before:
            print(f"[SUCCESS] Project '{name}' deleted successfully.")
        else:
            print("[ERROR] Project not found.")

    # -------------------------------
    # EDIT PROJECT (Phase 2)
    # -------------------------------
    def edit_project(self, name, new_name=None, new_description=None):
        project = self.find_project(name)
        if not project:
            return

        # check for duplicate name if changed
        if new_name and any(p.name.lower() == new_name.lower() for p in self.projects if p != project):
            print("[ERROR] Another project already has this name.")
            return

        project.edit(new_name, new_description)

    # -------------------------------
    # TASK METHODS
    # -------------------------------
    def add_task_to_project(self, project_name, title, description, deadline):
        project = self.find_project(project_name)
        if not project:
            return
        if len(project.tasks) >= self.max_tasks:
            print("[ERROR] Maximum number of tasks reached.")
            return

        task = Task(title, description, deadline)
        project.add_task(task)
        print(f"[SUCCESS] Task '{title}' added to project '{project_name}'.")

    def update_task_status(self, project_name, task_title, new_status):
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

    def delete_task_from_project(self, project_name, task_title):
        project = self.find_project(project_name)
        if not project:
            return
        project.delete_task(task_title)

    # -------------------------------
    # EDIT TASK (Phase 2)
    # -------------------------------
    def edit_task(self, project_name, task_title,
                  new_title=None, new_description=None,
                  new_deadline=None, new_status=None):
        project = self.find_project(project_name)
        if not project:
            return
        task = project.get_task(task_title)
        if not task:
            print("[ERROR] Task not found.")
            return
        task.edit(new_title, new_description, new_deadline, new_status)
