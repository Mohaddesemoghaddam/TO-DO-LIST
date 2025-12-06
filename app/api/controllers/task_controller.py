from fastapi import HTTPException
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse

from exceptions.service_exceptions import (
    TaskNotFoundError,
    TaskValidationError,
    TaskConflictError
)


class TaskController:
    def __init__(self, service):
        self.service = service

    # ------------------------------------------------------
    # CREATE
    # ------------------------------------------------------
    def create_task(self, data: TaskCreate):
        try:
            task = self.service.api_create_task(data)
            return TaskResponse.model_validate(task)
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except TaskConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # ------------------------------------------------------
    # GET
    # ------------------------------------------------------
    def get_task(self, task_id: int):
        try:
            task = self.service.api_get_task(task_id)
            return TaskResponse.model_validate(task)
        except TaskNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ------------------------------------------------------
    # LIST ALL
    # ------------------------------------------------------
    def list_tasks(self):
        try:
            tasks = self.service.api_list_tasks()
            return [TaskResponse.model_validate(t) for t in tasks]
        except Exception:
            raise HTTPException(status_code=500, detail="Server error")

    # ------------------------------------------------------
    # LIST OF PROJECT
    # ------------------------------------------------------
    def list_tasks_of_project(self, project_id: int):
        try:
            tasks = self.service.api_list_tasks_of_project(project_id)
            return [TaskResponse.model_validate(t) for t in tasks]
        except TaskNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ------------------------------------------------------
    # UPDATE
    # ------------------------------------------------------
    def update_task(self, task_id: int, data: TaskUpdate):
        try:
            updated = self.service.api_update_task(task_id, data)
            return {"updated": updated}
        except TaskNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except TaskConflictError as e:
            raise HTTPException(status_code=409, detail=str(e))

    # ------------------------------------------------------
    # DELETE
    # ------------------------------------------------------
    def delete_task(self, task_id: int):
        try:
            deleted = self.service.api_delete_task(task_id)
            if not deleted:
                raise TaskNotFoundError("Task not found")
            return {"deleted": True}
        except TaskNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))
