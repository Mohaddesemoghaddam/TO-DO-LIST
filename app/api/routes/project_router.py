from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db

from app.repositories.project_repository import ProjectRepository
from app.services.project_service import ProjectService
from app.api.controllers.project_controller import ProjectController

from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_controller(db: Session = Depends(get_db)):
    repo = ProjectRepository(db)
    service = ProjectService(repo)
    return ProjectController(service)


# -----------------------------
# CREATE PROJECT
# -----------------------------
@router.post("/", response_model=ProjectResponse, status_code=201)
def create_project(
    data: ProjectCreate,
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.create_project(data)


# -----------------------------
# LIST PROJECTS
# -----------------------------
@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.list_projects()


# -----------------------------
# GET ONE PROJECT
# -----------------------------
@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.get_project(project_id)


# -----------------------------
# UPDATE PROJECT
# -----------------------------
@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.update_project(project_id, data)


# -----------------------------
# DELETE PROJECT
# -----------------------------
@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.delete_project(project_id)


# -----------------------------
# LIST TASKS OF A PROJECT
# -----------------------------
@router.get("/{project_id}/tasks")
def list_project_tasks(
    project_id: int,
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.list_project_tasks(project_id)
