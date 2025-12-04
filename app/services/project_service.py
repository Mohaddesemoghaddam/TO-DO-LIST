from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse

from app.repositories.project_repository import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repository = repo

    def create_project(self, data: ProjectCreate):
        return self.repository.create(
            name=data.name,
            description=data.description
        )

    def get_project(self, project_id: int):
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")
        return project

    def list_projects(self):
        return self.repository.list_all()

    def update_project(self, project_id: int, data: ProjectUpdate):
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")

        return self.repository.update(
            project,
            name=data.name,
            description=data.description
        )

    def delete_project(self, project_id: int):
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")

        self.repository.delete(project)
        return True

    def list_tasks_of_project(self, project_id: int):
        project = self.repository.get_by_id(project_id)
        if not project:
            raise ValueError("Project not found")

        return project.tasks

