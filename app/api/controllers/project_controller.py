from fastapi import HTTPException
from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse


class ProjectController:
    def __init__(self, service):
        self.service = service

    def create_project(self, data: ProjectCreate):
        project = self.service.api_create_project(data)
        return ProjectResponse.model_validate(project)

    def list_projects(self):
        projects = self.service.api_list_projects()
        return [ProjectResponse.model_validate(p) for p in projects]

    def get_project(self, project_id: int):
        project = self.service.api_get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return ProjectResponse.model_validate(project)

    def update_project(self, project_id: int, data: ProjectUpdate):
        updated = self.service.api_update_project(project_id, data)
        return ProjectResponse.model_validate(updated)

    def delete_project(self, project_id: int):
        deleted = self.service.api_delete_project(project_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Project not found")

    def list_project_tasks(self, project_id: int):
        return self.service.api_list_tasks_of_project(project_id)
