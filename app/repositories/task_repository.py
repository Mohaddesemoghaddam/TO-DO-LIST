from sqlalchemy.orm import Session
from typing import List, Optional
from models.task import Task


class TaskRepository:
    """Handles all database operations for Task model."""

    # -------------------------------
    # CREATE
    # -------------------------------
    def create(self, db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    # -------------------------------
    # GET BY ID
    # -------------------------------
    def get_by_id(self, db: Session, task_id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()

    # -------------------------------
    # LIST ALL
    # -------------------------------
    def list_all(self, db: Session) -> List[Task]:
        return db.query(Task).all()

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update(self, db: Session, task: Task) -> Task:
        db.commit()
        db.refresh(task)
        return task

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete(self, db: Session, task: Task) -> None:
        db.delete(task)
        db.commit()

    # -------------------------------
    # LIST BY PROJECT
    # -------------------------------
    def list_by_project(self, db: Session, project_id: int) -> List[Task]:
        return db.query(Task).filter(Task.project_id == project_id).all()
