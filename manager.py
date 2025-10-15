# manager.py
import os
from dotenv import load_dotenv
from project import Project
from task import Task

load_dotenv()

class Manager:
    """Manages all projects and tasks with validation and in-memory storage."""

    def __init__(self):
        self.projects = []
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", 20))

    def add_project(self, name):
        if any(p.name.lower() == name.lower() for p in self.projects):
            raise ValueError("[ERROR] Project name already exists.")
        if len(self.projects) >= self.max_projects:
            raise ValueError("[ERROR] Maximum number of projects reached.")
        project = Project(name)
        self.projects.append(project)
        print(f"✅ Project '{name}' created successfully.")

    def show_all_projects(self):
        if not self.projects:
            print("No projects found.")
        for p in self.projects:
            print(p)

    def find_project(self, name):
        for p in self.projects:
            if p.name.lower() == name.lower():
                return p
        raise ValueError("[ERROR] Project not found.")

    def add_task_to_project(self, project_name, title, description, deadline):
        project = self.find_project(project_name)
        task = Task(title, description, deadline)
        project.add_task(task, self.max_tasks)
        print(f"✅ Task '{title}' added to project '{project_name}'.")

    def update_task_status(self, project_name, task_title, new_status):
        project = self.find_project(project_name)
        task = project.get_task(task_title)
        task.status = task._validate_status(new_status)
        print(f"✅ Updated '{task_title}' status to '{new_status}'.")

    def delete_task_from_project(self, project_name, task_title):
        project = self.find_project(project_name)
        project.remove_task(task_title)
        print(f"🗑️ Task '{task_title}' deleted from project '{project_name}'.")

    def delete_project(self, name):
        self.projects = [p for p in self.projects if p.name.lower() != name.lower()]
        print(f"🗑️ Project '{name}' deleted successfully.")
