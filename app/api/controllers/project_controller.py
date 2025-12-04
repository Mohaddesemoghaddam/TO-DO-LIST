from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse


class ProjectController:
    def __init__(self, service):
        self.service = service

    def create_project(self, data: ProjectCreate) -> ProjectResponse:
        project = self.service.create_project(data)
        return ProjectResponse.model_validate(project)

    def list_projects(self) -> list[ProjectResponse]:
        projects = self.service.list_projects()
        return [ProjectResponse.model_validate(p) for p in projects]

    def get_project(self, project_id: int) -> ProjectResponse:
        project = self.service.get_project(project_id)
        return ProjectResponse.model_validate(project)

    def update_project(self, project_id: int, data: ProjectUpdate) -> ProjectResponse:
        project = self.service.update_project(project_id, data)
        return ProjectResponse.model_validate(project)

    def delete_project(self, project_id: int):
        return self.service.delete_project(project_id)

    def list_project_tasks(self, project_id: int):
        return self.service.list_tasks_of_project(project_id)

