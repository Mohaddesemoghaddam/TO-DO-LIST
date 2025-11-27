from sqlalchemy.orm import Session

from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from db.session import SessionLocal

# Repository-layer exception (unused here but kept if needed)
# from exceptions.repository_exceptions import ObjectNotFoundError

from exceptions.service_exceptions import (
    ProjectNotFoundException,
    ProjectAlreadyExistsException
)


class ProjectService:
    def __init__(self):
        self.project_repo = ProjectRepository()
        self.task_repo = TaskRepository()

    # -----------------------------
    # Create Project
    # -----------------------------
    def create_project(self, name: str, description: str):
        with SessionLocal() as db:
            existing = self.project_repo.get_by_name(db, name)
            if existing:
                raise ProjectAlreadyExistsException(
                    f"Project '{name}' already exists."
                )

            return self.project_repo.create(
                db,
                name=name,
                description=description
            )

    # -----------------------------
    # Get All Projects
    # -----------------------------
    def get_all_projects(self):
        with SessionLocal() as db:
            return self.project_repo.get_all(db)

    # -----------------------------
    # Update Project
    # -----------------------------
    def update_project(self, old_name: str, new_name: str | None, new_desc: str | None):
        with SessionLocal() as db:
            project = self.project_repo.get_by_name(db, old_name)
            if not project:
                raise ProjectNotFoundException(f"Project '{old_name}' not found.")

            if new_name:
                duplicate = self.project_repo.get_by_name(db, new_name)
                if duplicate and duplicate.id != project.id:
                    raise ProjectAlreadyExistsException(
                        f"A project named '{new_name}' already exists."
                    )
                project.name = new_name

            if new_desc:
                project.description = new_desc

            return self.project_repo.update(db, project)

    # -----------------------------
    # Delete Project
    # -----------------------------
    def delete_project(self, name: str):
        with SessionLocal() as db:
            project = self.project_repo.get_by_name(db, name)
            if not project:
                raise ProjectNotFoundException(f"Project '{name}' not found.")

            tasks = self.task_repo.get_tasks_by_project(db, project.id)
            for t in tasks:
                self.task_repo.delete(db, t)

            return self.project_repo.delete(db, project)

    # -----------------------------
    # Get Tasks of a Project
    # -----------------------------
    def get_tasks_of_project(self, name: str):
        with SessionLocal() as db:
            project = self.project_repo.get_by_name(db, name)
            if not project:
                raise ProjectNotFoundException(f"Project '{name}' not found.")

            return self.task_repo.get_tasks_by_project(db, project.id)
