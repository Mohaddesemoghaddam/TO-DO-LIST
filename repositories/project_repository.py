# from sqlalchemy.orm import Session
# from repositories.base_repository import BaseRepository
# from models.project import Project


# class ProjectRepository(BaseRepository[Project]):
#     def __init__(self):
#         super().__init__(Project)

#     def get_by_name(self, db: Session, name: str):
#         return db.query(Project).filter(Project.name == name).first()
    
#     def get_by_id(self, project_id: int):
#         return self.db.query(Project).filter(Project.id == project_id).first()
# repositories/project_repository.py
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from models.project import Project


class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: Session):
        super().__init__(Project, db)

    def get_by_name(self, name: str):
        return self.db.query(Project).filter(Project.name == name).first()

    def get_by_id(self, project_id: int):  
        return self.db.query(Project).filter(Project.id == project_id).first()
