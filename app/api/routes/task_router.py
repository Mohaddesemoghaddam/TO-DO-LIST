# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from db.session import get_db
# from app.api.controllers.task_controller import TaskController
# from app.schemas.task.task_create import TaskCreate
# from app.schemas.task.task_replace import TaskReplace     
# from app.schemas.task.task_update import TaskUpdate       
# from app.schemas.task.task_response import TaskResponse
# from app.schemas.task.task_status_update import TaskStatusUpdate

# from services.task_service import TaskService


# router = APIRouter(
#     prefix="/projects/{project_name}/tasks",
#     tags=["Tasks"]
# )

# def get_task_controller(db: Session = Depends(get_db)):
#     service = TaskService(db)
#     return TaskController(service)


# @router.post("", response_model=TaskResponse, status_code=201)
# def create_task(project_name: str, data: TaskCreate,
#                 controller: TaskController = Depends(get_task_controller)):
#     return controller.create_task(project_name, data)


# @router.get("", response_model=list[TaskResponse])
# def list_tasks(project_name: str,
#                controller: TaskController = Depends(get_task_controller)):
#     return controller.list_tasks(project_name)



# @router.get("/{task_title}", response_model=TaskResponse)
# def get_task(project_name: str, task_title: str,
#              controller: TaskController = Depends(get_task_controller)):
#     return controller.get_task(project_name, task_title)

# @router.patch("/{task_title}", response_model=TaskResponse)
# def update_task(project_name: str, task_title: str, data: TaskUpdate,
#                 controller: TaskController = Depends(get_task_controller)):
#     return controller.update_task(project_name, task_title, data)

# @router.delete("/{task_title}", status_code=200)
# def delete_task(project_name: str, task_title: str,
#                 controller: TaskController = Depends(get_task_controller)):
#     controller.delete_task(project_name, task_title)
#     return {
#         "message": "Task deleted successfully",
#         "task_title": task_title
#     }



# @router.patch("/{task_title}/status", response_model=TaskResponse)
# def update_status(project_name: str, task_title: str, data: TaskStatusUpdate,
#                   controller: TaskController = Depends(get_task_controller)):
#     return controller.update_status(project_name, task_title, data)
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.task_service import TaskService
from app.api.controllers.task_controller import TaskController

from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_status_update import TaskStatusUpdate
from app.schemas.task.task_response import TaskResponse


router = APIRouter(
    prefix="/projects/{project_name}/tasks",
    tags=["Tasks"]
)


# -------------------------------------------------------
# Dependency Injection
# -------------------------------------------------------
def get_task_controller(db: Session = Depends(get_db)) -> TaskController:
    """Provides a TaskController instance with its TaskService dependency."""
    service = TaskService(db)
    return TaskController(service)


# -------------------------------------------------------
# CREATE TASK
# -------------------------------------------------------
@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    project_name: str,
    data: TaskCreate,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Create a new task within a project."""
    return controller.create_task(project_name, data)


# -------------------------------------------------------
# LIST TASKS
# -------------------------------------------------------
@router.get("", response_model=List[TaskResponse])
def list_tasks(
    project_name: str,
    controller: TaskController = Depends(get_task_controller)
) -> List[TaskResponse]:
    """Retrieve all tasks belonging to a specific project."""
    return controller.list_tasks(project_name)


# -------------------------------------------------------
# GET TASK
# -------------------------------------------------------
@router.get("/{task_title}", response_model=TaskResponse)
def get_task(
    project_name: str,
    task_title: str,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Retrieve a specific task by its title."""
    return controller.get_task(project_name, task_title)


# -------------------------------------------------------
# PATCH TASK (Partial Update)
# -------------------------------------------------------
@router.patch("/{task_title}", response_model=TaskResponse)
def update_task(
    project_name: str,
    task_title: str,
    data: TaskUpdate,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Partially update a task's fields."""
    return controller.update_task(project_name, task_title, data)


# -------------------------------------------------------
# PATCH STATUS ONLY
# -------------------------------------------------------
@router.patch("/{task_title}/status", response_model=TaskResponse)
def update_status(
    project_name: str,
    task_title: str,
    data: TaskStatusUpdate,
    controller: TaskController = Depends(get_task_controller)
) -> TaskResponse:
    """Update only the status of an existing task."""
    return controller.update_status(project_name, task_title, data)


# -------------------------------------------------------
# DELETE TASK
# -------------------------------------------------------
@router.delete("/{task_title}", status_code=200)
def delete_task(
    project_name: str,
    task_title: str,
    controller: TaskController = Depends(get_task_controller)
) -> dict:
    """Delete a task from a project by title."""
    controller.delete_task(project_name, task_title)
    return {
        "message": "Task deleted successfully.",
        "task_title": task_title
    }
