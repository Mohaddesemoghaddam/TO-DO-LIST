from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from models.project import Project


class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)

    def get_by_name(self, db: Session, name: str):
        return db.query(Project).filter(Project.name == name).first()
