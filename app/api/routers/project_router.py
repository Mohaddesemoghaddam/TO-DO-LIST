from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db

from repositories.project_repository import ProjectRepository
from services.project_service import ProjectService
from app.api.controllers.project_controller import ProjectController


from app.schemas.project.project_create import ProjectCreate
from app.schemas.project.project_update import ProjectUpdate
from app.schemas.project.project_response import ProjectResponse


router = APIRouter(prefix="/projects", tags=["Projects"])


def get_project_controller():
    repo = ProjectRepository()
    service = ProjectService(repo)
    return ProjectController(service)


@router.post("/", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.create_project(db, data)


@router.get("/", response_model=list[ProjectResponse])
def list_projects(
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.list_projects(db)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.get_project(db, project_id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.update_project(db, project_id, data)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.delete_project(db, project_id)


# special endpoint — list tasks of a project
@router.get("/{project_id}/tasks")
def list_project_tasks(
    project_id: int,
    db: Session = Depends(get_db),
    controller: ProjectController = Depends(get_project_controller)
):
    return controller.list_project_tasks(db, project_id)
