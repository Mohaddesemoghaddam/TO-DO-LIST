from sqlalchemy.orm import Session
from repositories.project_repository import ProjectRepository
from schemas.project.project_create import ProjectCreate
from schemas.project.project_update import ProjectUpdate


class ProjectService:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def create_project(self, db: Session, data: ProjectCreate):
        return self.repository.create(
            db,
            name=data.name,
            description=data.description
        )

    def get_project(self, db: Session, project_id: int):
        project = self.repository.get_by_id(db, project_id)
        if not project:
            raise ValueError("Project not found")
        return project

    def list_projects(self, db: Session):
        return self.repository.list_all(db)

    def update_project(self, db: Session, project_id: int, data: ProjectUpdate):
        project = self.repository.get_by_id(db, project_id)
        if not project:
            raise ValueError("Project not found")

        return self.repository.update(
            db,
            project,
            name=data.name,
            description=data.description
        )

    def delete_project(self, db: Session, project_id: int):
        project = self.repository.get_by_id(db, project_id)
        if not project:
            raise ValueError("Project not found")

        self.repository.delete(db, project)
        return True

    def list_tasks_of_project(self, db: Session, project_id: int):
        project = self.repository.get_by_id(db, project_id)
        if not project:
            raise ValueError("Project not found")

        return project.tasks
