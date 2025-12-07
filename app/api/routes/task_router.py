from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from app.api.controllers.task_controller import TaskController

from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_replace import TaskReplace     # PUT
from app.schemas.task.task_update import TaskUpdate       # PATCH
from app.schemas.task.task_response import TaskResponse
from app.schemas.task.task_status_update import TaskStatusUpdate

from services.task_service import TaskService


router = APIRouter(
    prefix="/projects/{project_name}/tasks",
    tags=["Tasks"]
)

def get_task_controller(db: Session = Depends(get_db)):
    service = TaskService(db)
    return TaskController(service)


# ---------------------
# POST
# ---------------------
@router.post("", response_model=TaskResponse, status_code=201)
def create_task(project_name: str, data: TaskCreate,
                controller: TaskController = Depends(get_task_controller)):
    return controller.create_task(project_name, data)


# ---------------------
# LIST
# ---------------------
@router.get("", response_model=list[TaskResponse])
def list_tasks(project_name: str,
               controller: TaskController = Depends(get_task_controller)):
    return controller.list_tasks(project_name)


# ---------------------
# GET ONE
# ---------------------
@router.get("/{task_title}", response_model=TaskResponse)
def get_task(project_name: str, task_title: str,
             controller: TaskController = Depends(get_task_controller)):
    return controller.get_task(project_name, task_title)


# # ---------------------
# # PUT (Full Replace)
# # ---------------------
# @router.put("/{task_title}", response_model=TaskResponse)
# def replace_task(project_name: str, task_title: str, data: TaskReplace,
#                  controller: TaskController = Depends(get_task_controller)):
#     return controller.replace_task(project_name, task_title, data)


# ---------------------
# PATCH (Partial Update)
# ---------------------
@router.patch("/{task_title}", response_model=TaskResponse)
def update_task(project_name: str, task_title: str, data: TaskUpdate,
                controller: TaskController = Depends(get_task_controller)):
    return controller.update_task(project_name, task_title, data)


# ---------------------
# DELETE
# ---------------------
@router.delete("/{task_title}", status_code=204)
def delete_task(project_name: str, task_title: str,
                controller: TaskController = Depends(get_task_controller)):
    controller.delete_task(project_name, task_title)
    return


# ---------------------
# PATCH STATUS (shortcut)
# ---------------------
@router.patch("/{task_title}/status", response_model=TaskResponse)
def update_status(project_name: str, task_title: str, data: TaskStatusUpdate,
                  controller: TaskController = Depends(get_task_controller)):
    return controller.update_status(project_name, task_title, data)
