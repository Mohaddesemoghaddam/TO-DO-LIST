from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.project_service import ProjectService
from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse



class ProjectController:
    def __init__(self, service: ProjectService):
        self.service = service

    def create_project(self, db: Session, data: ProjectCreate):
        try:
            return self.service.create_project(db, data)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_project(self, db: Session, project_id: int):
        try:
            return self.service.get_project(db, project_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Project not found")

    def list_projects(self, db: Session):
        return self.service.list_projects(db)

    def update_project(self, db: Session, project_id: int, data: ProjectUpdate):
        try:
            return self.service.update_project(db, project_id, data)
        except ValueError:
            raise HTTPException(status_code=404, detail="Project not found")

    def delete_project(self, db: Session, project_id: int):
        try:
            self.service.delete_project(db, project_id)
            return {"message": "Project deleted successfully"}
        except ValueError:
            raise HTTPException(status_code=404, detail="Project not found")

    def list_project_tasks(self, db: Session, project_id: int):
        try:
            return self.service.list_tasks_of_project(db, project_id)
        except ValueError:
            raise HTTPException(status_code=404, detail="Project not found")
