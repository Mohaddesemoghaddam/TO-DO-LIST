# # from sqlalchemy.orm import Session

# # from repositories.project_repository import ProjectRepository
# # from repositories.task_repository import TaskRepository
# # from db.session import SessionLocal

# # # Repository-layer exception (unused here but kept if needed)
# # # from exceptions.repository_exceptions import ObjectNotFoundError

# # from exceptions.service_exceptions import (
# #     ProjectNotFoundException,
# #     ProjectAlreadyExistsException
# # )


# # class ProjectService:
# #     def __init__(self, db=None):
# #         if db is None:
# #             from db.session import SessionLocal
# #             db = SessionLocal()
# #         self.db = db
# #         self.repo = ProjectRepository(db)



# #     # -----------------------------
# #     # Create Project
# #     # -----------------------------
# #     def create_project(self, name: str, description: str):
# #         with SessionLocal() as db:
# #             existing = self.project_repo.get_by_name(db, name)
# #             if existing:
# #                 raise ProjectAlreadyExistsException(
# #                     f"Project '{name}' already exists."
# #                 )

# #             return self.project_repo.create(
# #                 db,
# #                 name=name,
# #                 description=description
# #             )

# #     # -----------------------------
# #     # Get All Projects
# #     # -----------------------------
# #     def get_all_projects(self):
# #         with SessionLocal() as db:
# #             return self.project_repo.get_all(db)

# #     # -----------------------------
# #     # Update Project
# #     # -----------------------------
# #     def update_project(self, old_name: str, new_name: str | None, new_desc: str | None):
# #         with SessionLocal() as db:
# #             project = self.project_repo.get_by_name(db, old_name)
# #             if not project:
# #                 raise ProjectNotFoundException(f"Project '{old_name}' not found.")

# #             if new_name:
# #                 duplicate = self.project_repo.get_by_name(db, new_name)
# #                 if duplicate and duplicate.id != project.id:
# #                     raise ProjectAlreadyExistsException(
# #                         f"A project named '{new_name}' already exists."
# #                     )
# #                 project.name = new_name

# #             if new_desc:
# #                 project.description = new_desc

# #             return self.project_repo.update(db, project)

# #     # -----------------------------
# #     # Delete Project
# #     # -----------------------------
# #     def delete_project(self, name: str):
# #         with SessionLocal() as db:
# #             project = self.project_repo.get_by_name(db, name)
# #             if not project:
# #                 raise ProjectNotFoundException(f"Project '{name}' not found.")

# #             tasks = self.task_repo.get_tasks_by_project(db, project.id)
# #             for t in tasks:
# #                 self.task_repo.delete(db, t)

# #             return self.project_repo.delete(db, project)

# #     # -----------------------------
# #     # Get Tasks of a Project
# #     # -----------------------------
# #     def get_tasks_of_project(self, name: str):
# #         with SessionLocal() as db:
# #             project = self.project_repo.get_by_name(db, name)
# #             if not project:
# #                 raise ProjectNotFoundException(f"Project '{name}' not found.")

# #             return self.task_repo.get_tasks_by_project(db, project.id)
    
# #     def api_get_project(self, project_id: int):
# #         return self.repo.get_by_id(project_id)
# from repositories.project_repository import ProjectRepository
# from repositories.task_repository import TaskRepository
# from db.session import SessionLocal

# from exceptions.service_exceptions import (
#     ProjectNotFoundException,
#     ProjectAlreadyExistsException
# )


# class ProjectService:
#     def __init__(self, db=None):
#         if db is None:
#             db = SessionLocal()
#         self.db = db
#         self.repo = ProjectRepository(db)
#         self.project_repo = ProjectRepository(db)
#         self.task_repo = TaskRepository(db)

#     # -----------------------------
#     # CLI: create project
#     # -----------------------------
#     def create_project(self, name: str, description: str):

#         existing = self.project_repo.get_by_name(name)
#         if existing:
#             raise ProjectAlreadyExistsException(
#                 f"Project '{name}' already exists."
#             )

#         return self.project_repo.create(
#             name=name,
#             description=description
#         )

#     # -----------------------------
#     # CLI: get all projects
#     # -----------------------------
#     def get_all_projects(self):
#         return self.project_repo.get_all()

#     # -----------------------------
#     # CLI: update project
#     # -----------------------------
#     def update_project(self, old_name: str, new_name: str | None, new_desc: str | None):

#         project = self.project_repo.get_by_name(old_name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{old_name}' not found.")

#         if new_name:
#             duplicate = self.project_repo.get_by_name(new_name)
#             if duplicate and duplicate.id != project.id:
#                 raise ProjectAlreadyExistsException(
#                     f"A project named '{new_name}' already exists."
#                 )
#             project.name = new_name

#         if new_desc:
#             project.description = new_desc

#         return self.project_repo.update(project)

#     # -----------------------------
#     # CLI: delete project
#     # -----------------------------
#     def delete_project(self, name: str):

#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{name}' not found.")

#         tasks = self.task_repo.get_tasks_by_project(project.id)
#         for t in tasks:
#             self.task_repo.delete(t)

#         return self.project_repo.delete(project)

#     # -----------------------------
#     # CLI: get tasks of project
#     # -----------------------------
#     def get_tasks_of_project(self, name: str):

#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise ProjectNotFoundException(f"Project '{name}' not found.")

#         return self.task_repo.get_tasks_by_project(project.id)

#     # -----------------------------
#     # API: get project by ID
#     # -----------------------------
#     def api_get_project(self, project_id: int):
#         project = self.project_repo.get_by_id(project_id)
#         if not project:
#             raise ProjectNotFoundException(f"Project with ID {project_id} not found.")
#         return project
# services/project_service.py

# from sqlalchemy.orm import Session
# from db.session import SessionLocal
# from repositories.project_repository import ProjectRepository
# from fastapi import HTTPException

# class ProjectService:

#     def __init__(self, db=None):
#         # اگر DB از API تزریق شد:
#         if db is not None:
#             self.db = db
#         else:
#             # اگر از CLI فراخوانی شد:
#             self.db = SessionLocal()

#         self.project_repo = ProjectRepository(self.db)

#     # ---------------------------
#     # CLI METHODS (name-based)
#     # ---------------------------

#     def add_project(self, name: str, description: str):
#         existing = self.project_repo.get_by_name(name)
#         if existing:
#             raise Exception("Project already exists with this name.")
#         return self.project_repo.create(name=name, description=description)

#     def get_all_projects(self):
#         return self.project_repo.get_all()

#     def get_project_by_name(self, name: str):
#         return self.project_repo.get_by_name(name)

#     def edit_project(self, name: str, new_name=None, new_desc=None):
#         project = self.project_repo.get_by_name(name)
#         if not project:
#             raise Exception("Project not found.")

#         updates = {}
#         if new_name:
#             updates["name"] = new_name
#         if new_desc:
#             updates["description"] = new_desc

#         return self.project_repo.update(project, **updates)

#     def delete_project(self, name: str):
#         project = self.project_repo.get_by_name(name)

#         if not project:
#             raise HTTPException(status_code=404, detail="Project not found")

#         # حذف با شیء، نه ID
#         return self.project_repo.delete(project)

#     # ---------------------------
#     # API METHODS (ID-based)
#     # ---------------------------

#     def api_create_project(self, data):
#         return self.project_repo.create(
#             name=data.name,
#             description=data.description
#         )

#     def api_get_project(self, project_id: int):
#         project = self.project_repo.get_by_id(project_id)
#         if not project:
#             raise HTTPException(status_code=404, detail="Project not found")
#         return project

#     def api_update_project(self, project_id: int, data):
#         project = self.project_repo.get_by_id(project_id)
#         if not project:
#             raise HTTPException(status_code=404, detail="Project not found")

#         updates = {}
#         if data.name is not None:
#             updates["name"] = data.name
#         if data.description is not None:
#             updates["description"] = data.description

#         return self.project_repo.update(project, **updates)

#     def api_delete_project(self, project_id: int):
#         project = self.project_repo.get_by_id(project_id)
#         if not project:
#             raise HTTPException(status_code=404, detail="Project not found")

#         self.project_repo.delete(project)
#         return True

#     def api_list_tasks_of_project(self, project_id: int):
#         from services.task_service import TaskService

#         project = self.project_repo.get_by_id(project_id)
#         if not project:
#             raise HTTPException(status_code=404, detail="Project not found")

#         task_service = TaskService(db=self.db)
#         return task_service.task_repo.get_tasks_by_project_id(project_id)
   
#     def api_list_projects(self):
#         return self.project_repo.get_all()
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
    def edit_project(self, name, new_name=None, new_desc=None):
        project = self.project_repo.get_by_name(name)
        if not project:
            raise ProjectNotFoundError(f"Project '{name}' not found.")

        if new_name:
            existing = self.project_repo.get_by_name(new_name)
            if existing and existing.id != project.id:
                raise ProjectConflictError(f"Project '{new_name}' already exists.")
            project.name = new_name

        if new_desc:
            project.description = new_desc

        return self.project_repo.update(project)

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


