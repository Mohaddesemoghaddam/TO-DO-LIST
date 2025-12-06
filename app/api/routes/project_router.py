from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import get_db
from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse

from services.project_service import ProjectService
from app.api.controllers.project_controller import ProjectController

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_controller(db: Session = Depends(get_db)):
    service = ProjectService(db)
    return ProjectController(service)


# CREATE
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(data: ProjectCreate,
                   controller: ProjectController = Depends(get_project_controller)):
    return controller.create_project(data)


# LIST
@router.get("/", response_model=list[ProjectResponse])
def list_projects(controller: ProjectController = Depends(get_project_controller)):
    return controller.list_projects()


# GET ONE
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int,
                controller: ProjectController = Depends(get_project_controller)):
    project = controller.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


# UPDATE
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int,
                   data: ProjectUpdate,
                   controller: ProjectController = Depends(get_project_controller)):
    return controller.update_project(project_id, data)


# DELETE
@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int,
                   controller: ProjectController = Depends(get_project_controller)):
    controller.delete_project(project_id)
    return {"message": "Project deleted successfully"}


# LIST TASKS OF PROJECT
@router.get("/{project_id}/tasks")
def list_project_tasks(project_id: int,
                       controller: ProjectController = Depends(get_project_controller)):
    return controller.list_project_tasks(project_id)
