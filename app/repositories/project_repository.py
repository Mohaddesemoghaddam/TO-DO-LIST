from sqlalchemy.orm import Session
from models.project import Project

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, description: str | None):
        project = Project(name=name, description=description)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project

    def get_by_id(self, project_id: int):
        return self.db.query(Project).filter(Project.id == project_id).first()

    def list_all(self):
        return self.db.query(Project).all()

    def update(self, project: Project, name: str | None, description: str | None):
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description
        self.db.commit()
        self.db.refresh(project)
        return project

    def delete(self, project: Project):
        self.db.delete(project)
        self.db.commit()
