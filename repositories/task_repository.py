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
# from repositories.base_repository import BaseRepository
# from models.task import Task
# from models.project import Project
# from datetime import date
# from sqlalchemy.orm import Session
# from sqlalchemy import and_


# class TaskRepository(BaseRepository[Task]):
#     def __init__(self, db: Session):
#         super().__init__(Task, db)

#     def get_overdue_tasks(self):
#         today = date.today()
#         return (
#             self.db.query(Task)
#             .filter(and_(Task.deadline < today, Task.status != "done"))
#             .all()
#         )

#     def get_tasks_by_project(self, project_id: int):
#         return self.db.query(Task).filter(Task.project_id == project_id).all()

#     def get_task_by_title(self, project_id: int, title: str):
#         return (
#             self.db.query(Task)
#             .filter(Task.project_id == project_id)
#             .filter(Task.title == title)
#             .first()
#         )

#     def get_by_id(self, task_id: int):
#         return self.db.query(Task).filter(Task.id == task_id).first()

#     def get_tasks_by_project_id(self, project_id: int):
#         return (
#             self.db.query(Task)
#             .filter(Task.project_id == project_id)
#             .all()
#         )

#     # -----------------------------------------
#     # NEW: Name-Based (REAL RESTFUL)
#     # -----------------------------------------
#     def get_tasks_by_project_name(self, project_name: str):
#         return (
#             self.db.query(Task)
#             .join(Project, Task.project_id == Project.id)
#             .filter(Project.name == project_name)
#             .all()
        # )
from sqlalchemy.orm import Session
from models.task import Task
from models.project import Project


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------------------------
    # Create
    # ----------------------------------------------------
    def create(self, title, description, deadline, status, project_id):
        task = Task(
            title=title,
            description=description,
            deadline=deadline,
            status=status,
            project_id=project_id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # ----------------------------------------------------
    # Read
    # ----------------------------------------------------
    def get_task_by_title(self, project_id, title):
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id, Task.title == title)
            .first()
        )

    def get_tasks_by_project_name(self, project_name: str):
        return (
            self.db.query(Task)
            .join(Project, Task.project_id == Project.id)
            .filter(Project.name == project_name)
            .all()
        )

    def get_task_by_project_name_and_title(self, project_name: str, task_title: str):
        return (
            self.db.query(Task)
            .join(Project, Task.project_id == Project.id)
            .filter(Project.name == project_name, Task.title == task_title)
            .first()
        )

    # ----------------------------------------------------
    # Update
    # ----------------------------------------------------
    def update(self, task: Task):
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # ----------------------------------------------------
    # Delete
    # ----------------------------------------------------
    def delete(self, task: Task):
        self.db.delete(task)
        self.db.commit()
