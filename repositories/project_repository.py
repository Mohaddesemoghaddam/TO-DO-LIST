from repositories.base_repository import BaseRepository
from models.project import Project

class ProjectRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)
