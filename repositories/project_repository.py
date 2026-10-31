# from sqlalchemy.orm import Session
# from repositories.base_repository import BaseRepository
# from models.project import Project


# class ProjectRepository(BaseRepository[Project]):
#     def __init__(self, db: Session):
#         super().__init__(Project, db)

#     def get_by_name(self, name: str):
#         return self.db.query(Project).filter(Project.name == name).first()

#     def get_by_id(self, project_id: int):  
#         return self.db.query(Project).filter(Project.id == project_id).first()
from typing import Optional, List
from sqlalchemy.orm import Session
from repositories.base_repository import BaseRepository
from models.project import Project


class ProjectRepository(BaseRepository[Project]):
    """
    Repository layer for handling database operations related to Project entity.
    Performs pure CRUD operations — no business logic.
    """

    def __init__(self, db: Session):
        """
        Initialize ProjectRepository with a SQLAlchemy database session.
        """
        super().__init__(Project, db)

    # ----------------------------------------------------
    # READ OPERATIONS
    # ----------------------------------------------------
    def get_by_name(self, name: str) -> Optional[Project]:
        """
        Retrieve a project by its unique name.
        """
        return (
            self.db.query(Project)
            .filter(Project.name == name.strip())
            .first()
        )

    def get_by_id(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a project by its unique ID.
        """
        return (
            self.db.query(Project)
            .filter(Project.id == project_id)
            .first()
        )

    def get_all(self) -> List[Project]:
        """
        Retrieve all projects from the database.
        """
        return self.db.query(Project).all()

    # ----------------------------------------------------
    # DELETE BY NAME (optional helper)
    # ----------------------------------------------------
    def delete_by_name(self, name: str) -> None:
        """
        Delete a project by name.
        """
        project = self.get_by_name(name)
        if project:
            self.db.delete(project)
            self.db.commit()
