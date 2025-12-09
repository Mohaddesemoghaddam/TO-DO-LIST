# from fastapi import HTTPException
# from services.task_service import TaskService
# from exceptions.service_exceptions import (
#     TaskNotFoundException,
#     TaskValidationError,
#     ProjectNotFoundException
# )

# class TaskController:
#     def __init__(self, service: TaskService):
#         self.service = service

    
#     def create_task(self, project_name, data):
#         try:
#             return self.service.create_task(project_name, data)
#         except ProjectNotFoundException as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except TaskValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))

    
#     def list_tasks(self, project_name):
#         try:
#             return self.service.list_tasks(project_name)
#         except ProjectNotFoundException as e:
#             raise HTTPException(status_code=404, detail=str(e))
    

    
#     def get_task(self, project_name, task_title):
#         try:
#             return self.service.get_task(project_name, task_title)
#         except (ProjectNotFoundException, TaskNotFoundException) as e:
#             raise HTTPException(status_code=404, detail=str(e))



#     def update_task(self, project_name, task_title, data):
#         try:
#             return self.service.update_task(project_name, task_title, data)
#         except (ProjectNotFoundException, TaskNotFoundException) as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except TaskValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))


#     def delete_task(self, project_name, task_title):
#         try:
#             self.service.delete_task(project_name, task_title)
#         except (ProjectNotFoundException, TaskNotFoundException) as e:
#             raise HTTPException(status_code=404, detail=str(e))


#     def update_status(self, project_name, task_title, data):
#         try:
#             return self.service.update_status(project_name, task_title, data.status)
#         except (ProjectNotFoundException, TaskNotFoundException) as e:
#             raise HTTPException(status_code=404, detail=str(e))
#         except TaskValidationError as e:
#             raise HTTPException(status_code=400, detail=str(e))
from fastapi import HTTPException
from services.task_service import TaskService
from exceptions.service_exceptions import (
    TaskNotFoundException,
    TaskValidationError,
    ProjectNotFoundException,
)


class TaskController:
    """Controller layer for task-related operations."""

    def __init__(self, service: TaskService):
        """Initialize TaskController with its corresponding service."""
        self.service: TaskService = service

    # ----------------------------------------------------
    # CREATE TASK
    # ----------------------------------------------------
    def create_task(self, project_name: str, data) -> object:
        """Create a new task in a project."""
        try:
            return self.service.create_task(project_name, data)
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ----------------------------------------------------
    # LIST TASKS
    # ----------------------------------------------------
    def list_tasks(self, project_name: str) -> list:
        """Retrieve all tasks belonging to the given project."""
        try:
            return self.service.list_tasks(project_name)
        except ProjectNotFoundException as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ----------------------------------------------------
    # GET TASK
    # ----------------------------------------------------
    def get_task(self, project_name: str, task_title: str) -> object:
        """Retrieve a specific task by its title."""
        try:
            return self.service.get_task(project_name, task_title)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))

    # ----------------------------------------------------
    # PATCH TASK (Partial Update)
    # ----------------------------------------------------
    def update_task(self, project_name: str, task_title: str, data) -> object:
        """Partially update a task’s details."""
        try:
            return self.service.update_task(project_name, task_title, data)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ----------------------------------------------------
    # PATCH STATUS ONLY
    # ----------------------------------------------------
    def update_status(self, project_name: str, task_title: str, data) -> object:
        """Update only the status of a task."""
        try:
            return self.service.update_status(project_name, task_title, data.status)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
        except TaskValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

    # ----------------------------------------------------
    # DELETE TASK
    # ----------------------------------------------------
    def delete_task(self, project_name: str, task_title: str) -> None:
        """Delete a task by title."""
        try:
            self.service.delete_task(project_name, task_title)
        except (ProjectNotFoundException, TaskNotFoundException) as e:
            raise HTTPException(status_code=404, detail=str(e))
