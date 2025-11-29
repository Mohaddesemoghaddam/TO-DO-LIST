from sqlalchemy.orm import Session
from models.project import Project


class ProjectRepository:

    def create(self, db: Session, name: str, description: str | None):
        project = Project(name=name, description=description)
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    def get_by_id(self, db: Session, project_id: int):
        return db.query(Project).filter(Project.id == project_id).first()

    def list_all(self, db: Session):
        return db.query(Project).all()

    def update(self, db: Session, project: Project, name: str | None, description: str | None):
        if name is not None:
            project.name = name
        if description is not None:
            project.description = description

        db.commit()
        db.refresh(project)
        return project

    def delete(self, db: Session, project: Project):
        db.delete(project)
        db.commit()
