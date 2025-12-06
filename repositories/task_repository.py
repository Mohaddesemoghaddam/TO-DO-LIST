# from repositories.base_repository import BaseRepository
# from models.task import Task
# from datetime import date
# from sqlalchemy.orm import Session
# from sqlalchemy import and_

# class TaskRepository(BaseRepository[Task]):
#     def __init__(self):
#         super().__init__(Task)

#     def get_overdue_tasks(self, db: Session):
#         today = date.today()
#         return (
#             db.query(Task)
#             .filter(and_(Task.deadline < today, Task.status != "done"))
#             .all()
#         )

#     def get_tasks_by_project(self, db: Session, project_id: int):
#         return db.query(Task).filter(Task.project_id == project_id).all()

#     def get_task_by_title(self, db: Session, project_id: int, title: str):
#         return (
#             db.query(Task)
#             .filter(Task.project_id == project_id)
#             .filter(Task.title == title)
#             .first()
#         )
#     def get_by_id(self, task_id: int):
#         return self.db.query(Task).filter(Task.id == task_id).first()
# repositories/task_repository.py
from repositories.base_repository import BaseRepository
from models.task import Task
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_


class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: Session):
        super().__init__(Task, db)

    def get_overdue_tasks(self):
        today = date.today()
        return (
            self.db.query(Task)
            .filter(and_(Task.deadline < today, Task.status != "done"))
            .all()
        )

    def get_tasks_by_project(self, project_id: int):
        return self.db.query(Task).filter(Task.project_id == project_id).all()

    def get_task_by_title(self, project_id: int, title: str):
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .filter(Task.title == title)
            .first()
        )

    def get_by_id(self, task_id: int):
        return self.db.query(Task).filter(Task.id == task_id).first()
    
    def get_tasks_by_project_id(self, project_id: int):
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id)
            .all()
        )
