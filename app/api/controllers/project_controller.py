# from fastapi import HTTPException
# from app.schemas.project.project_create import ProjectCreate
# from app.schemas.project.project_update import ProjectUpdate
# from app.schemas.project.project_response import ProjectResponse

# from exceptions.service_exceptions import (
#     ProjectNotFoundError,
#     ProjectValidationError,
#     ProjectConflictError
# )


# class ProjectController:
#     def __init__(self, service):
#         self.service = service

#     # ------------------------------------------------------
#     # CREATE
#     # ------------------------------------------------------
#     def create_project(self, data: ProjectCreate):
#         try:
#             project = self.service.api_create_project(data)
#             return ProjectResponse.model_validate(project)
#         except ProjectValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))
#         except ProjectConflictError as e:
#             raise HTTPException(status_code=409, detail=str(e))

#     # ------------------------------------------------------
#     # LIST ALL
#     # ------------------------------------------------------
#     def list_projects(self):
#         try:
#             projects = self.service.api_list_projects()
#             return [ProjectResponse.model_validate(p) for p in projects]
#         except Exception:
#             raise HTTPException(status_code=500, detail="Server error")

#     # ------------------------------------------------------
#     # GET ONE
#     # ------------------------------------------------------
#     def get_project(self, project_id: int):
#         try:
#             project = self.service.api_get_project_by_id(project_id)
#             return ProjectResponse.model_validate(project)
#         except ProjectNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))

#     # ------------------------------------------------------
#     # UPDATE
#     # ------------------------------------------------------
#     def update_project(self, project_id: int, data: ProjectUpdate):
#         try:
#             updated = self.service.api_update_project(project_id, data)
#             return ProjectResponse.model_validate(updated)
#         except ProjectNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except ProjectValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))
#         except ProjectConflictError as e:
#             raise HTTPException(status_code=409, detail=str(e))

#     # ------------------------------------------------------
#     # DELETE
#     # ------------------------------------------------------
#     def delete_project(self, project_id: int):
#         try:
#             deleted = self.service.api_delete_project(project_id)
#             if not deleted:
#                 raise ProjectNotFoundError("Project not found")
#             return {"deleted": True}
#         except ProjectNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))

#     # ------------------------------------------------------
#     # LIST PROJECT TASKS
#     # ------------------------------------------------------
#     def list_project_tasks(self, project_id: int):
#         try:
#             tasks = self.service.api_list_tasks_of_project(project_id)
#             return tasks
#         except ProjectNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))
from fastapi import HTTPException

from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse

from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectConflictError,
)


class ProjectController:
    def __init__(self, service):
        self.service = service

    # CREATE
    def create_project(self, data: ProjectCreate):
        try:
            project = self.service.add_project(data.name, data.description)
            return ProjectResponse.model_validate(project)
        except ProjectValidationError as e:
            raise HTTPException(400, str(e))
        except ProjectConflictError as e:
            raise HTTPException(409, str(e))

    # LIST
    def list_projects(self):
        projects = self.service.get_all_projects()
        return [ProjectResponse.model_validate(p) for p in projects]

    # GET ONE
    def get_project(self, name: str):
        try:
            project = self.service.get_project_by_name(name)
            return ProjectResponse.model_validate(project)
        except ProjectNotFoundError as e:
            raise HTTPException(404, str(e))

    # UPDATE
    def update_project(self, name: str, data: ProjectUpdate):
        try:
            updated = self.service.edit_project(
                name,
                new_name=data.name,
                new_desc=data.description
            )
            return ProjectResponse.model_validate(updated)
        except ProjectNotFoundError as e:
            raise HTTPException(404, str(e))
        except ProjectValidationError as e:
            raise HTTPException(400, str(e))
        except ProjectConflictError as e:
            raise HTTPException(409, str(e))

    # DELETE
    def delete_project(self, name: str):
        try:
            self.service.delete_project(name)
            return {"deleted": True}
        except ProjectNotFoundError as e:
            raise HTTPException(404, str(e))

    # LIST TASKS
    def list_project_tasks(self, name: str):
        try:
            return self.service.list_tasks_of_project(name)
        except ProjectNotFoundError as e:
            raise HTTPException(404, str(e))
