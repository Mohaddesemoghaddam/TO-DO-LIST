from db.session import SessionLocal
from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository

from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectConflictError,
)


class ProjectService:

    def __init__(self, db=None):
        self.db = db or SessionLocal()
        self.project_repo = ProjectRepository(self.db)
        self.task_repo = TaskRepository(self.db)

    # CREATE
    def add_project(self, name: str, description: str):
        name = name.strip()

        if len(name) < 3:
            raise ProjectValidationError("Project name must be at least 3 characters.")

        existing = self.project_repo.get_by_name(name)
        if existing:
            raise ProjectConflictError(f"Project '{name}' already exists.")

        return self.project_repo.create(name=name, description=description)

    # LIST
    def get_all_projects(self):
        return self.project_repo.get_all()

    # GET ONE
    def get_project_by_name(self, name: str):
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")
        return project

    # UPDATE
    # def edit_project(self, name, new_name=None, new_desc=None):
    #     project = self.project_repo.get_by_name(name)
    #     if not project:
    #         raise ProjectNotFoundError(f"Project '{name}' not found.")

    #     if new_name:
    #         existing = self.project_repo.get_by_name(new_name)
    #         if existing and existing.id != project.id:
    #             raise ProjectConflictError(f"Project '{new_name}' already exists.")
    #         project.name = new_name

    #     if new_desc:
    #         project.description = new_desc

    #     return self.project_repo.update(project)

    def edit_project(self, name, new_name=None, new_desc=None, is_replace=False):
        project = self.get_project_by_name(name)

    # PUT → replace everything
        if is_replace:
             project.name = new_name
             project.description = new_desc
             self.db.commit()
             self.db.refresh(project)
             return project

    # PATCH → only update provided fields
        if new_name is not None:
            project.name = new_name
        if new_desc is not None:
           project.description = new_desc

        self.db.commit()
        self.db.refresh(project)
        return project


    # DELETE
    def delete_project(self, name):
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")
        return self.project_repo.delete(project)

    # LIST TASKS
    def list_tasks_of_project(self, name):
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")

        tasks = self.task_repo.get_tasks_by_project_name(name)
        return tasks


