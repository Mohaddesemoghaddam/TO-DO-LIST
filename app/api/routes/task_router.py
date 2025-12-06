# from fastapi import APIRouter, Depends
# from app.api.controllers.task_controller import TaskController
# from services.task_service import TaskService
# from app.schemas.task.task_create import TaskCreate
# from app.schemas.task.task_update import TaskUpdate
# from app.schemas.task.task_response import TaskResponse


# router = APIRouter(prefix="/tasks", tags=["Tasks"])


# def get_task_controller():
#     service = TaskService()
#     controller = TaskController(service)
#     return controller


# @router.post("/", response_model=TaskResponse, status_code=201)
# def create_task(data: TaskCreate, controller = Depends(get_task_controller)):
#     return controller.create_task(data)


# @router.get("/{task_id}", response_model=TaskResponse)
# def get_task(task_id: int, controller = Depends(get_task_controller)):
#     return controller.get_task(task_id)


# @router.get("/", response_model=list[TaskResponse])
# def list_tasks(controller = Depends(get_task_controller)):
#     return controller.list_tasks()




# @router.put("/{task_id}", response_model=TaskResponse)
# def update_task(task_id: int, data: TaskUpdate, controller = Depends(get_task_controller)):
#     return controller.update_task(task_id, data)


# @router.delete("/{task_id}", status_code=204)
# def delete_task(task_id: int, controller = Depends(get_task_controller)):
#     return controller.delete_task(task_id)


# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from db.session import get_db

# from app.api.controllers.task_controller import TaskController
# from app.schemas.task.task_create import TaskCreate
# from app.schemas.task.task_update import TaskUpdate
# from app.schemas.task.task_response import TaskResponse
# from app.schemas.task.task_status_update import TaskStatusUpdate

# from services.task_service import TaskService


# router = APIRouter(
#     prefix="/projects/{project_name}/tasks",
#     tags=["Tasks"]
# )


# # Dependency injector for controller
# def get_task_controller(db: Session = Depends(get_db)):
#     service = TaskService(db)
#     return TaskController(service)


# # Create Task
# @router.post("", response_model=TaskResponse, status_code=201)
# def create_task(project_name: str, data: TaskCreate, controller: TaskController = Depends(get_task_controller)):
#     return controller.create_task(project_name, data)


# # List Tasks of a Project
# @router.get("", response_model=list[TaskResponse])
# def list_tasks(project_name: str, controller: TaskController = Depends(get_task_controller)):
#     return controller.list_tasks(project_name)


# # Get Single Task
# @router.get("/{task_title}", response_model=TaskResponse)
# def get_task(project_name: str, task_title: str, controller: TaskController = Depends(get_task_controller)):
#     return controller.get_task(project_name, task_title)


# # Update Task
# @router.put("/{task_title}", response_model=TaskResponse)
# def update_task(project_name: str, task_title: str, data: TaskUpdate, controller: TaskController = Depends(get_task_controller)):
#     return controller.update_task(project_name, task_title, data)


# # Delete Task
# @router.delete("/{task_title}", status_code=204)
# def delete_task(project_name: str, task_title: str, controller: TaskController = Depends(get_task_controller)):
#     controller.delete_task(project_name, task_title)
#     return


# # Update Only Task Status
# @router.patch("/{task_title}/status", response_model=TaskResponse)
# def update_status(project_name: str, task_title: str, data: TaskStatusUpdate, controller: TaskController = Depends(get_task_controller)):
#     return controller.update_status(project_name, task_title, data)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

from app.api.controllers.task_controller import TaskController
from app.schemas.task.task_create import TaskCreate
from app.schemas.task.task_update import TaskUpdate
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


# Create
@router.post("", response_model=TaskResponse, status_code=201)
def create_task(project_name: str, data: TaskCreate,
                controller: TaskController = Depends(get_task_controller)):
    return controller.create_task(project_name, data)


# List
@router.get("", response_model=list[TaskResponse])
def list_tasks(project_name: str,
               controller: TaskController = Depends(get_task_controller)):
    return controller.list_tasks(project_name)


# Get One
@router.get("/{task_title}", response_model=TaskResponse)
def get_task(project_name: str, task_title: str,
             controller: TaskController = Depends(get_task_controller)):
    return controller.get_task(project_name, task_title)


# Update
@router.put("/{task_title}", response_model=TaskResponse)
def update_task(project_name: str, task_title: str, data: TaskUpdate,
                controller: TaskController = Depends(get_task_controller)):
    return controller.update_task(project_name, task_title, data)


# Delete
@router.delete("/{task_title}", status_code=204)
def delete_task(project_name: str, task_title: str,
                controller: TaskController = Depends(get_task_controller)):
    controller.delete_task(project_name, task_title)
    return


# Update Status
@router.patch("/{task_title}/status", response_model=TaskResponse)
def update_status(project_name: str, task_title: str, data: TaskStatusUpdate,
                  controller: TaskController = Depends(get_task_controller)):
    return controller.update_status(project_name, task_title, data)
