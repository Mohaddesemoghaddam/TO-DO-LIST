from sqlalchemy.orm import Session
from typing import List
from models.task import Task
from repositories.task_repository import TaskRepository
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse



class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repo = repository

    # -------------------------------
    # CREATE
    # -------------------------------
    def create_task(self, db: Session, data: TaskCreate) -> Task:
        new_task = Task(
            title=data.title,
            description=data.description,
            deadline=data.deadline,
            status=data.status,
            project_id=data.project_id
        )
        return self.repo.create(db, new_task)

    # -------------------------------
    # GET BY ID
    # -------------------------------
    def get_task(self, db: Session, task_id: int) -> Task:
        task = self.repo.get_by_id(db, task_id)
        if not task:
            raise ValueError("Task not found")
        return task

    # -------------------------------
    # LIST ALL
    # -------------------------------
    def list_tasks(self, db: Session) -> List[Task]:
        return self.repo.list_all(db)

    # -------------------------------
    # LIST BY PROJECT
    # -------------------------------
    def list_tasks_of_project(self, db: Session, project_id: int) -> List[Task]:
        return self.repo.list_by_project(db, project_id)

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update_task(self, db: Session, task_id: int, data: TaskUpdate) -> Task:
        task = self.get_task(db, task_id)

        if data.title is not None:
            task.title = data.title

        if data.description is not None:
            task.description = data.description

        if data.deadline is not None:
            task.deadline = data.deadline

        if data.status is not None:
            if data.status not in Task.VALID_STATUSES:
                raise ValueError(f"Invalid status. Use one of: {Task.VALID_STATUSES}")
            task.status = data.status

        return self.repo.update(db, task)

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete_task(self, db: Session, task_id: int) -> None:
        task = self.get_task(db, task_id)
        self.repo.delete(db, task)
