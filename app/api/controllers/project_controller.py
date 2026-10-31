# from fastapi import HTTPException
# from app.schemas.project.project_create import ProjectCreate
# from app.schemas.project.project_update import ProjectUpdate
# from app.schemas.project.project_response import ProjectResponse
# from app.schemas.project.project_replace import ProjectReplace

# from exceptions.service_exceptions import (
#     ProjectNotFoundError,
#     ProjectValidationError,
#     ProjectConflictError,
# )


# class ProjectController:
#     def __init__(self, service):
#         self.service = service

#     # CREATE
#     def create_project(self, data: ProjectCreate):
#         try:
#             project = self.service.add_project(data.name, data.description)
#             return ProjectResponse.model_validate(project)
#         except ProjectValidationError as e:
#             raise HTTPException(400, str(e))
#         except ProjectConflictError as e:
#             raise HTTPException(409, str(e))

#     # LIST
#     def list_projects(self):
#         projects = self.service.get_all_projects()
#         return [ProjectResponse.model_validate(p) for p in projects]

#     # GET ONE
#     def get_project(self, name: str):
#         try:
#             project = self.service.get_project_by_name(name)
#             return ProjectResponse.model_validate(project)
#         except ProjectNotFoundError as e:
#             raise HTTPException(404, str(e))

#     # -------------------------------------------------------
#     # PUT → Full Replace
#     # -------------------------------------------------------
#     def replace_project(self, name: str, data: ProjectReplace):
#         try:
#             updated = self.service.edit_project(
#                 name=name,
#                 new_name=data.name,             # اگر None باشد → عمداً None
#                 new_desc=data.description,      # اگر None باشد → عمداً None
#                 is_replace=True                 # FLAAAAG → یعنی PUT
#             )
#             return ProjectResponse.model_validate(updated)

#         except ProjectNotFoundError as e:
#             raise HTTPException(404, str(e))
#         except ProjectValidationError as e:
#             raise HTTPException(400, str(e))
#         except ProjectConflictError as e:
#             raise HTTPException(409, str(e))

#     # -------------------------------------------------------
#     # PATCH → Partial Update
#     # -------------------------------------------------------
#     def patch_project(self, name: str, data: ProjectUpdate):
#         try:
#             updated = self.service.edit_project(
#                 name=name,
#                 new_name=data.new_name,             # only if not None
#                 new_desc=data.new_description,      # only if not None
#                 is_replace=False                    # PATCH behavior
#             )
#             return ProjectResponse.model_validate(updated)

#         except ProjectNotFoundError as e:
#             raise HTTPException(404, str(e))
#         except ProjectValidationError as e:
#             raise HTTPException(400, str(e))
#         except ProjectConflictError as e:
#             raise HTTPException(409, str(e))

#     # DELETE
#     def delete_project(self, name: str):
#         try:
#             self.service.delete_project(name)
#             return {"deleted": True}
#         except ProjectNotFoundError as e:
#             raise HTTPException(404, str(e))

#     # LIST TASKS
#     def list_project_tasks(self, name: str):
#         try:
#             return self.service.list_tasks_of_project(name)
#         except ProjectNotFoundError as e:
#             raise HTTPException(404, str(e))
from typing import List
from fastapi import HTTPException
from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse
from app.schemas.project.project_replace import ProjectReplace
from services.project_service import ProjectService
from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectConflictError,
)


class ProjectController:
    """Controller layer handling API interactions for Project entity."""

    def __init__(self, service: ProjectService):
        """Constructor Injection - receives a ProjectService instance."""
        self.service: ProjectService = service

    # -------------------------------------------------------
    # CREATE
    # -------------------------------------------------------
    def create_project(self, data: ProjectCreate) -> ProjectResponse:
        """Create a new project using validated input."""
        try:
            project = self.service.add_project(data.name, data.description)
            return ProjectResponse.model_validate(project)
        except ProjectValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ProjectConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # -------------------------------------------------------
    # LIST ALL
    # -------------------------------------------------------
    def list_projects(self) -> List[ProjectResponse]:
        """Retrieve a list of all projects."""
        projects = self.service.get_all_projects()
        return [ProjectResponse.model_validate(p) for p in projects]

    # -------------------------------------------------------
    # GET ONE
    # -------------------------------------------------------
    def get_project(self, name: str) -> ProjectResponse:
        """Retrieve a single project by its name."""
        try:
            project = self.service.get_project_by_name(name)
            return ProjectResponse.model_validate(project)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # -------------------------------------------------------
    # PUT → Full Replace
    # -------------------------------------------------------
    def replace_project(self, name: str, data: ProjectReplace) -> ProjectResponse:
        """Replace a project's name and description (PUT behavior)."""
        try:
            updated = self.service.edit_project(
                name=name,
                new_name=data.name,
                new_desc=data.description,
                is_replace=True
            )
            return ProjectResponse.model_validate(updated)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ProjectValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ProjectConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # -------------------------------------------------------
    # PATCH → Partial Update
    # -------------------------------------------------------
    def patch_project(self, name: str, data: ProjectUpdate) -> ProjectResponse:
        """Partially update project details (PATCH behavior)."""
        try:
            updated = self.service.edit_project(
                name=name,
                new_name=data.new_name,
                new_desc=data.new_description,
                is_replace=False
            )
            return ProjectResponse.model_validate(updated)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ProjectValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ProjectConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # -------------------------------------------------------
    # DELETE
    # -------------------------------------------------------
    def delete_project(self, name: str) -> dict:
        """Delete a project by name."""
        try:
            self.service.delete_project(name)
            return {"deleted": True}
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # -------------------------------------------------------
    # LIST TASKS
    # -------------------------------------------------------
    def list_project_tasks(self, name: str):
        """List all tasks belonging to a specific project."""
        try:
            return self.service.list_tasks_of_project(name)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
