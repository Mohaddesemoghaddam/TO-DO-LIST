# from fastapi import HTTPException
# from app.schemas.task.task_create import TaskCreate
# from app.schemas.task.task_update import TaskUpdate
# from app.schemas.task.task_response import TaskResponse

# from exceptions.service_exceptions import (
#     TaskNotFoundError,
#     TaskValidationError,
#     TaskConflictError
# )


# class TaskController:
#     def __init__(self, service):
#         self.service = service

#     # ------------------------------------------------------
#     # CREATE
#     # ------------------------------------------------------
#     def create_task(self, data: TaskCreate):
#         try:
#             task = self.service.api_create_task(data)
#             return TaskResponse.model_validate(task)
#         except TaskValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))
#         except TaskConflictError as e:
#             raise HTTPException(status_code=409, detail=str(e))

#     # ------------------------------------------------------
#     # GET
#     # ------------------------------------------------------
#     def get_task(self, task_id: int):
#         try:
#             task = self.service.api_get_task(task_id)
#             return TaskResponse.model_validate(task)
#         except TaskNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))

#     # ------------------------------------------------------
#     # LIST ALL
#     # ------------------------------------------------------
#     def list_tasks(self):
#         try:
#             tasks = self.service.api_list_tasks()
#             return [TaskResponse.model_validate(t) for t in tasks]
#         except Exception:
#             raise HTTPException(status_code=500, detail="Server error")

#     # ------------------------------------------------------
#     # LIST OF PROJECT
#     # ------------------------------------------------------
#     def list_tasks_of_project(self, project_id: int):
#         try:
#             tasks = self.service.api_list_tasks_of_project(project_id)
#             return [TaskResponse.model_validate(t) for t in tasks]
#         except TaskNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))

#     # ------------------------------------------------------
#     # UPDATE
#     # ------------------------------------------------------
#     def update_task(self, task_id: int, data: TaskUpdate):
#         try:
#             updated = self.service.api_update_task(task_id, data)
#             return {"updated": updated}
#         except TaskNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except TaskValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))
#         except TaskConflictError as e:
#             raise HTTPException(status_code=409, detail=str(e))

#     # ------------------------------------------------------
#     # DELETE
#     # ------------------------------------------------------
#     def delete_task(self, task_id: int):
#         try:
#             deleted = self.service.api_delete_task(task_id)
#             if not deleted:
#                 raise TaskNotFoundError("Task not found")
#             return {"deleted": True}
#         except TaskNotFoundError as e:
#             raise HTTPException(status_code=404, detail=str(e))
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

    # Create
    def create_task(self, project_name, data):
        try:
            return self.service.add_task_to_project(
                project_name=project_name,
                title=data.title,
                description=data.description,
                deadline=data.deadline,
            )
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # List
    def list_tasks(self, project_name):
        try:
            return self.service.list_tasks_of_project(project_name)
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    # Get one
    def get_task(self, project_name, task_title):
        try:
            return self.service.get_task(project_name, task_title)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))

    # Update
    def update_task(self, project_name, task_title, data):
        try:
            return self.service.edit_task(
                project_name=project_name,
                task_title=task_title,
                new_title=data.title,
                new_desc=data.description,
                new_deadline=data.deadline,
                new_status=data.status,
            )
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # Delete
    def delete_task(self, project_name, task_title):
        try:
            self.service.delete_task(project_name, task_title)
            return None  # For HTTP 204
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))

    # Update Status (PATCH)
    def update_status(self, project_name, task_title, data):
        try:
            return self.service.update_status(
                project_name=project_name,
                task_title=task_title,
                new_status=data.status,
            )
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

