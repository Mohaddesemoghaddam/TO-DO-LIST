# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from db.session import get_db
# from services.project_service import ProjectService
# from app.api.controllers.project_controller import ProjectController

# from app.schemas.project.project_create import ProjectCreate
# from app.schemas.project.project_update import ProjectUpdate
# from app.schemas.project.project_response import ProjectResponse
# from app.schemas.project.project_replace import ProjectReplace

# router = APIRouter(prefix="/projects", tags=["Projects"])


# def get_controller(db: Session = Depends(get_db)):
#     service = ProjectService(db)
#     return ProjectController(service)


# # CREATE
# @router.post("", response_model=ProjectResponse, status_code=201)
# def create_project(data: ProjectCreate, controller: ProjectController = Depends(get_controller)):
#     return controller.create_project(data)


# # LIST
# @router.get("", response_model=list[ProjectResponse])
# def list_projects(controller: ProjectController = Depends(get_controller)):
#     return controller.list_projects()


# # GET ONE
# @router.get("/{project_name}", response_model=ProjectResponse)
# def get_project(project_name: str, controller: ProjectController = Depends(get_controller)):
#     return controller.get_project(project_name)


# # # PUT → Replace
# # @router.put("/{project_name}", response_model=ProjectResponse)
# # def replace_project(project_name: str, data: ProjectReplace, controller: ProjectController = Depends(get_controller)):
# #     return controller.replace_project(project_name, data)


# # PATCH → Partial Update
# @router.patch("/{project_name}", response_model=ProjectResponse)
# def update_project(project_name: str, data: ProjectUpdate, controller: ProjectController = Depends(get_controller)):
#     return controller.patch_project(project_name, data)


# # DELETE
# @router.delete("/{project_name}", status_code=200)
# def delete_project(project_name: str, controller: ProjectController = Depends(get_controller)):
#     controller.delete_project(project_name)
#     return {
#         "message": "Project deleted successfully",
#         "project_name": project_name
#     }


# # LIST TASKS OF PROJECT
# @router.get("/{project_name}/tasks")
# def list_project_tasks(project_name: str, controller: ProjectController = Depends(get_controller)):
#     return controller.list_project_tasks(project_name)
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from services.project_service import ProjectService
from app.api.controllers.project_controller import ProjectController

from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse
from app.schemas.project.project_replace import ProjectReplace

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_controller(db: Session = Depends(get_db)) -> ProjectController:
    """Dependency injection for ProjectController."""
    service = ProjectService(db)
    return ProjectController(service)


# -------------------------------------------------------
# CREATE PROJECT
# -------------------------------------------------------
@router.post("", response_model=ProjectResponse, status_code=201)
def create_project(
    data: ProjectCreate,
    controller: ProjectController = Depends(get_controller)
) -> ProjectResponse:
    """Create a new project."""
    return controller.create_project(data)


# -------------------------------------------------------
# LIST ALL PROJECTS
# -------------------------------------------------------
@router.get("", response_model=List[ProjectResponse])
def list_projects(controller: ProjectController = Depends(get_controller)) -> List[ProjectResponse]:
    """Retrieve all existing projects."""
    return controller.list_projects()


# -------------------------------------------------------
# GET ONE PROJECT
# -------------------------------------------------------
@router.get("/{project_name}", response_model=ProjectResponse)
def get_project(
    project_name: str,
    controller: ProjectController = Depends(get_controller)
) -> ProjectResponse:
    """Retrieve a single project by its name."""
    return controller.get_project(project_name)


# -------------------------------------------------------
# PATCH PROJECT → Partial Update
# -------------------------------------------------------
@router.patch("/{project_name}", response_model=ProjectResponse)
def update_project(
    project_name: str,
    data: ProjectUpdate,
    controller: ProjectController = Depends(get_controller)
) -> ProjectResponse:
    """Partially update the fields of a project."""
    return controller.patch_project(project_name, data)


# -------------------------------------------------------
# DELETE PROJECT
# -------------------------------------------------------
@router.delete("/{project_name}", status_code=200)
def delete_project(
    project_name: str,
    controller: ProjectController = Depends(get_controller)
) -> dict:
    """Delete a project by name."""
    controller.delete_project(project_name)
    return {
        "message": "Project deleted successfully.",
        "project_name": project_name
    }


# -------------------------------------------------------
# LIST PROJECT TASKS
# -------------------------------------------------------
@router.get("/{project_name}/tasks")
def list_project_tasks(
    project_name: str,
    controller: ProjectController = Depends(get_controller)
) -> list:
    """List all tasks belonging to a specific project."""
    return controller.list_project_tasks(project_name)
