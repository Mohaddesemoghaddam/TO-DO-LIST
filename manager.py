# manager.py
import os
from project import Project
from task import Task

class Manager:
    """
    Handles in-memory management of projects and tasks.
    """
    def __init__(self):
        self.projects: list[Project] = []
        self.max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))
        self.max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", 20))
        self.project_counter = 1
        self.task_counter = 1

    # ---------- Project Methods ----------
    def create_project(self, name: str, description: str):
        if len(self.projects) >= self.max_projects:
            raise ValueError("Maximum number of projects reached.")
        if any(p.name == name for p in self.projects):
            raise ValueError("A project with this name already exists.")
        project = Project(self.project_counter, name, description)
        self.projects.append(project)
        self.project_counter += 1
        return project

    def list_projects(self):
        if not self.projects:
            return ["No projects found."]
        return [str(p) for p in self.projects]

    def edit_project(self, project_id: int, new_name=None, new_description=None):
        project = self._get_project(project_id)
        if new_name and any(p.name == new_name for p in self.projects if p.id != project_id):
            raise ValueError("Duplicate project name not allowed.")
        if new_name:
            project.name = new_name
        if new_description:
            project.description = new_description
        return project

    def delete_project(self, project_id: int):
        self.projects = [p for p in self.projects if p.id != project_id]

    # ---------- Task Methods ----------
    def add_task(self, project_id: int, title: str, description: str, deadline: str):
        project = self._get_project(project_id)
        if len(project.tasks) >= self.max_tasks:
            raise ValueError("Max number of tasks reached for this project.")
        task = Task(self.task_counter, title, description, deadline)
        self.task_counter += 1
        project.add_task(task)
        return task

    def list_tasks(self, project_id: int):
        project = self._get_project(project_id)
        return project.list_tasks() if project.tasks else ["No tasks found."]

    def edit_task(self, project_id: int, task_id: int, **kwargs):
        project = self._get_project(project_id)
        for task in project.tasks:
            if task.id == task_id:
                task.update(**kwargs)
                return task
        raise ValueError("Task not found.")

    def delete_task(self, project_id: int, task_id: int):
        project = self._get_project(project_id)
        project.remove_task(task_id)

    # ---------- Helpers ----------
    def _get_project(self, project_id: int) -> Project:
        for project in self.projects:
            if project.id == project_id:
                return project
        raise ValueError("Project not found.")
