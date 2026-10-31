# import os
# from db.session import SessionLocal
# from repositories.project_repository import ProjectRepository
# from repositories.task_repository import TaskRepository
# from exceptions.service_exceptions import (
#     ProjectNotFoundError,
#     ProjectValidationError,
#     ProjectConflictError,
# )


# MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))


# class ProjectService:

#     def __init__(self, db=None):
#         self.db = db or SessionLocal()
#         self.project_repo = ProjectRepository(self.db)
#         self.task_repo = TaskRepository(self.db)

#     # CREATE
#     def add_project(self, name: str, description: str):
#         name = name.strip()

#         if len(name) < 3:
#             raise ProjectValidationError("Project name must be at least 3 characters.")

#         existing = self.project_repo.get_by_name(name)
#         if existing:
#             raise ProjectConflictError(f"Project '{name}' already exists.")

#         # ✅ بررسی سقف مجاز پروژه‌ها
#         current_count = len(self.project_repo.get_all())
#         if current_count >= MAX_NUMBER_OF_PROJECT:
#             raise ProjectConflictError(
#                 f"Maximum number of projects ({MAX_NUMBER_OF_PROJECT}) reached. "
#                 "Cannot create more projects."
#             )

#         return self.project_repo.create(name=name, description=description)

#     # LIST
#     def get_all_projects(self):
#         return self.project_repo.get_all()

#     # GET ONE
#     def get_project_by_name(self, name: str):
#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise ProjectNotFoundError(f"Project '{name}' not found.")
#         return project

#     # UPDATE (PUT / PATCH)
#     def edit_project(self, name, new_name=None, new_desc=None, is_replace=False):
#         project = self.get_project_by_name(name)

#         # PUT → replace everything
#         if is_replace:
#             project.name = new_name
#             project.description = new_desc
#             self.db.commit()
#             self.db.refresh(project)
#             return project

#         # PATCH → only update provided fields
#         if new_name is not None:
#             project.name = new_name
#         if new_desc is not None:
#             project.description = new_desc

#         self.db.commit()
#         self.db.refresh(project)
#         return project

#     # DELETE
#     def delete_project(self, name):
#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise ProjectNotFoundError(f"Project '{name}' not found.")
#         return self.project_repo.delete(project)

#     # LIST TASKS
#     def list_tasks_of_project(self, name):
#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise ProjectNotFoundError(f"Project '{name}' not found.")

#         tasks = self.task_repo.get_tasks_by_project_name(name)
#         return tasks

from typing import Optional, List
from sqlalchemy.orm import Session
import os

from models.project import Project
from repositories.project_repository import ProjectRepository
from repositories.task_repository import TaskRepository
from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectConflictError,
)

# 🔧 مقدار پیش‌فرض برای سقف تعداد پروژه‌ها
MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", 5))


class ProjectService:
    """Business logic layer for managing projects."""

    def __init__(self, db: Session):
        """
        Constructor Injection:
        Dependencies (Session + Repositories) are passed in from the outside.
        """
        self.db: Session = db
        self.project_repo: ProjectRepository = ProjectRepository(db)
        self.task_repo: TaskRepository = TaskRepository(db)

    # ---------------------- CREATE ---------------------- #
    def add_project(self, name: str, description: str) -> Project:
        """Create a new project if validation & limit checks pass."""
        name = name.strip()

        if len(name) < 3:
            raise ProjectValidationError("Project name must be at least 3 characters.")

        if self.project_repo.get_by_name(name):
            raise ProjectConflictError(f"Project '{name}' already exists.")

        current_count = len(self.project_repo.get_all())
        if current_count >= MAX_NUMBER_OF_PROJECT:
            raise ProjectConflictError(
                f"Maximum number of projects ({MAX_NUMBER_OF_PROJECT}) reached."
            )

        return self.project_repo.create(name=name, description=description)

    # ---------------------- READ ALL ---------------------- #
    def get_all_projects(self) -> List[Project]:
        """Return all projects."""
        return self.project_repo.get_all()

    # ---------------------- READ ONE ---------------------- #
    def get_project_by_name(self, name: str) -> Project:
        """Return a single project by its name."""
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")
        return project

    # ---------------------- UPDATE ---------------------- #
    def edit_project(
        self,
        name: str,
        new_name: Optional[str] = None,
        new_desc: Optional[str] = None,
        is_replace: bool = False,
    ) -> Project:
        """Update project information (partial or full)."""
        project = self.get_project_by_name(name)

        if is_replace:
            project.name = new_name or project.name
            project.description = new_desc or project.description
        else:
            if new_name:
                project.name = new_name
            if new_desc:
                project.description = new_desc

        self.db.commit()
        self.db.refresh(project)
        return project

    # ---------------------- DELETE ---------------------- #
    def delete_project(self, name: str) -> None:
        """Delete project if exists."""
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")
        self.project_repo.delete(project)

    # ---------------------- RELATED TASKS ---------------------- #
    def list_tasks_of_project(self, name: str) -> List:
        """Return all tasks belonging to the given project."""
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")

        return self.task_repo.get_tasks_by_project_name(name)

