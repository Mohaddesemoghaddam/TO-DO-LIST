from repositories.base_repository import BaseRepository
from models.task import Task

class TaskRepository(BaseRepository[Task]):
    def __init__(self):
        super().__init__(Task)
