from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.task_service import TaskService
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse



class TaskController:
    def __init__(self, service: TaskService):
        self.service = service

    # -------------------------------
    # CREATE
    # -------------------------------
    def create_task(self, db: Session, data: TaskCreate) -> TaskResponse:
        try:
            task = self.service.create_task(db, data)
            return TaskResponse.model_validate(task)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    # -------------------------------
    # GET BY ID
    # -------------------------------
    def get_task(self, db: Session, task_id: int) -> TaskResponse:
        try:
            task = self.service.get_task(db, task_id)
            return TaskResponse.model_validate(task)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    # -------------------------------
    # LIST ALL
    # -------------------------------
    def list_tasks(self, db: Session) -> list[TaskResponse]:
        tasks = self.service.list_tasks(db)
        return [TaskResponse.model_validate(t) for t in tasks]

    # -------------------------------
    # LIST BY PROJECT
    # -------------------------------
    def list_tasks_of_project(self, db: Session, project_id: int) -> list[TaskResponse]:
        tasks = self.service.list_tasks_of_project(db, project_id)
        return [TaskResponse.model_validate(t) for t in tasks]

    # -------------------------------
    # UPDATE
    # -------------------------------
    def update_task(self, db: Session, task_id: int, data: TaskUpdate) -> TaskResponse:
        try:
            task = self.service.update_task(db, task_id, data)
            return TaskResponse.model_validate(task)
        except ValueError as e:
            if "not found" in str(e).lower():
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    # -------------------------------
    # DELETE
    # -------------------------------
    def delete_task(self, db: Session, task_id: int) -> dict:
        try:
            self.service.delete_task(db, task_id)
            return {"message": "Task deleted successfully"}
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
