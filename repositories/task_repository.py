
# from sqlalchemy.orm import Session
# from models.task import Task
# from models.project import Project


# class TaskRepository:
#     def __init__(self, db: Session):
#         self.db = db

#     # ----------------------------------------------------
#     # Create
#     # ----------------------------------------------------
#     def create(self, title, description, deadline, status, project_id):
#         task = Task(
#             title=title,
#             description=description,
#             deadline=deadline,
#             status=status,
#             project_id=project_id
#         )
#         self.db.add(task)
#         self.db.commit()
#         self.db.refresh(task)
#         return task

#     # ----------------------------------------------------
#     # Read
#     # ----------------------------------------------------
#     def get_task_by_title(self, project_id, title):
#         return (
#             self.db.query(Task)
#             .filter(Task.project_id == project_id, Task.title == title)
#             .first()
#         )

#     def get_tasks_by_project_name(self, project_name: str):
#         return (
#             self.db.query(Task)
#             .join(Project, Task.project_id == Project.id)
#             .filter(Project.name == project_name)
#             .all()
#         )

#     def get_task_by_project_name_and_title(self, project_name: str, task_title: str):
#         return (
#             self.db.query(Task)
#             .join(Project, Task.project_id == Project.id)
#             .filter(Project.name == project_name, Task.title == task_title)
#             .first()
#         )

#     # ----------------------------------------------------
#     # Update
#     # ----------------------------------------------------
#     def update(self, task: Task):
#         self.db.add(task)
#         self.db.commit()
#         self.db.refresh(task)
#         return task

#     # ----------------------------------------------------
#     # Delete
#     # ----------------------------------------------------
#     def delete(self, task: Task):
#         self.db.delete(task)
#         self.db.commit()
from sqlalchemy.orm import Session
from models.task import Task
from models.project import Project
from typing import List, Optional


class TaskRepository:
    """
    Repository layer for database operations related to Task entity.

    Handles raw CRUD operations without any business logic.
    """

    def __init__(self, db: Session):
        """
        Initialize TaskRepository with a SQLAlchemy session.
        """
        self.db = db

    # ----------------------------------------------------
    # CREATE
    # ----------------------------------------------------
    def create(self, title: str, description: str, deadline: str,
               status: str, project_id: int) -> Task:
        """
        Create and persist a new Task in the database.
        """
        task = Task(
            title=title.strip(),
            description=description.strip(),
            deadline=deadline,
            status=status.lower().strip(),
            project_id=project_id
        )
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # ----------------------------------------------------
    # READ
    # ----------------------------------------------------
    def get_task_by_title(self, project_id: int, title: str) -> Optional[Task]:
        """
        Retrieve a task by title and project ID.
        """
        return (
            self.db.query(Task)
            .filter(Task.project_id == project_id, Task.title == title.strip())
            .first()
        )

    def get_tasks_by_project_name(self, project_name: str) -> List[Task]:
        """
        Retrieve all tasks related to a specific project name.
        """
        return (
            self.db.query(Task)
            .join(Project, Task.project_id == Project.id)
            .filter(Project.name == project_name.strip())
            .all()
        )

    def get_task_by_project_name_and_title(self, project_name: str, task_title: str) -> Optional[Task]:
        """
        Retrieve a single task by project name and task title.
        """
        return (
            self.db.query(Task)
            .join(Project, Task.project_id == Project.id)
            .filter(Project.name == project_name.strip(), Task.title == task_title.strip())
            .first()
        )

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------
    def update(self, task: Task) -> Task:
        """
        Update an existing task and persist changes to the database.
        """
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------
    def delete(self, task: Task) -> None:
        """
        Remove a task from the database.
        """
        self.db.delete(task)
        self.db.commit()
