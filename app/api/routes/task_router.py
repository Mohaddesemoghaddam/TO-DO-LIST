from fastapi import APIRouter, Depends
from app.api.controllers.task_controller import TaskController
from services.task_service import TaskService
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
from app.schemas.task.task_response import TaskResponse


router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_task_controller():
    service = TaskService()
    controller = TaskController(service)
    return controller


@router.post("/", response_model=TaskResponse, status_code=201)
def create_task(data: TaskCreate, controller = Depends(get_task_controller)):
    return controller.create_task(data)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, controller = Depends(get_task_controller)):
    return controller.get_task(task_id)


@router.get("/", response_model=list[TaskResponse])
def list_tasks(controller = Depends(get_task_controller)):
    return controller.list_tasks()


@router.get("/project/{project_id}", response_model=list[TaskResponse])
def list_tasks_of_project(project_id: int, controller = Depends(get_task_controller)):
    return controller.list_tasks_of_project(project_id)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, controller = Depends(get_task_controller)):
    return controller.update_task(task_id, data)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, controller = Depends(get_task_controller)):
    return controller.delete_task(task_id)
