from fastapi import HTTPException
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse


class TaskController:
    def __init__(self, service):
        self.service = service

    def create_task(self, data: TaskCreate):
        task = self.service.api_create_task(data)
        return TaskResponse.model_validate(task)

    def get_task(self, task_id: int):
        task = self.service.api_get_task(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskResponse.model_validate(task)

    def list_tasks(self):
        tasks = self.service.api_list_tasks()
        return [TaskResponse.model_validate(t) for t in tasks]

    def list_tasks_of_project(self, project_id: int):
        tasks = self.service.api_list_tasks_of_project(project_id)
        return [TaskResponse.model_validate(t) for t in tasks]

    def update_task(self, task_id: int, data: TaskUpdate):
        updated = self.service.api_update_task(task_id, data)
        return TaskResponse.model_validate(updated)

    def delete_task(self, task_id: int):
        deleted = self.service.api_delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
