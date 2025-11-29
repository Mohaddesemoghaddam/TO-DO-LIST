from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

from app.api.controllers.task_controller import TaskController
from app.services.task_service import TaskService
from app.repositories.task_repository import TaskRepository

from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_controller():
    repo = TaskRepository()
    service = TaskService(repo)
    controller = TaskController(service)
    return controller


@router.post("/", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.create_task(db, data)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.get_task(db, task_id)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.list_tasks(db)


@router.get("/project/{project_id}", response_model=list[TaskResponse])
def list_tasks_of_project(
    project_id: int,
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.list_tasks_of_project(db, project_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.update_task(db, task_id, data)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    controller: TaskController = Depends(get_task_controller),
):
    return controller.delete_task(db, task_id)
