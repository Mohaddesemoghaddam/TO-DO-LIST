from db.session import get_db
from models.task import Task
from repositories.base_repository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, session=None):
        super().__init__(session or get_db(), Task)
