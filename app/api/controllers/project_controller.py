from fastapi import HTTPException
from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse

from exceptions.service_exceptions import (
    ProjectNotFoundError,
    ProjectValidationError,
    ProjectConflictError
)


class ProjectController:
    def __init__(self, service):
        self.service = service

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------
    def create_project(self, data: ProjectCreate):
        try:
            project = self.service.api_create_project(data)
            return ProjectResponse.model_validate(project)
        except ProjectValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ProjectConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # ------------------------------------------------------
    # LIST ALL
    # ------------------------------------------------------
    def list_projects(self):
        try:
            projects = self.service.api_list_projects()
            return [ProjectResponse.model_validate(p) for p in projects]
        except Exception:
            raise HTTPException(status_code=500, detail="Server error")

    # ------------------------------------------------------
    # GET ONE
    # ------------------------------------------------------
    def get_project(self, project_id: int):
        try:
            project = self.service.api_get_project_by_id(project_id)
            return ProjectResponse.model_validate(project)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------
    def update_project(self, project_id: int, data: ProjectUpdate):
        try:
            updated = self.service.api_update_project(project_id, data)
            return ProjectResponse.model_validate(updated)
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except ProjectValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except ProjectConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------
    def delete_project(self, project_id: int):
        try:
            deleted = self.service.api_delete_project(project_id)
            if not deleted:
                raise ProjectNotFoundError("Project not found")
            return {"deleted": True}
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ------------------------------------------------------
    # LIST PROJECT TASKS
    # ------------------------------------------------------
    def list_project_tasks(self, project_id: int):
        try:
            tasks = self.service.api_list_tasks_of_project(project_id)
            return tasks
        except ProjectNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
