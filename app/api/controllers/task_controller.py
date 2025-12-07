from fastapi import HTTPException
from services.task_service import TaskService
from exceptions.service_exceptions import (
    TaskNotFoundException,
    TaskValidationError,
    ProjectNotFoundException
)


class TaskController:
    def __init__(self, service: TaskService):
        self.service = service

    
    def create_task(self, project_name, data):
        try:
            return self.service.create_task(project_name, data)
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    
    def list_tasks(self, project_name):
        try:
            return self.service.list_tasks(project_name)
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    
    def get_task(self, project_name, task_title):
        try:
            return self.service.get_task(project_name, task_title)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))

    
    # # ---------------------------
    # # PUT → Full Replace
    # # ---------------------------
    # def replace_task(self, project_name, task_title, data):
    #     try:
    #         return self.service.replace_task(project_name, task_title, data)
    #     except (ProjectNotFoundException, TaskNotFoundException) as e:
    #         raise HTTPException(status_code=404, detail=str(e))
    #     except TaskValidationError as e:
    #         raise HTTPException(status_code=400, detail=str(e))


    # ---------------------------
    # PATCH → Partial Update
    # ---------------------------
    def update_task(self, project_name, task_title, data):
        try:
            return self.service.update_task(project_name, task_title, data)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))


    def delete_task(self, project_name, task_title):
        try:
            self.service.delete_task(project_name, task_title)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))


    def update_status(self, project_name, task_title, data):
        try:
            return self.service.update_status(project_name, task_title, data.status)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
