from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db
from app.services.user_service import UserService
from app.api.controllers.user_controller import UserController

from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_update import UserUpdate
from app.schemas.user.user_response import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    service = UserService(db)
    controller = UserController(service)
    return controller


@router.post("/", response_model=UserResponse)
def create_user(data: UserCreate, controller: UserController = Depends(get_user_controller)):
    return controller.create_user(data)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    return controller.get_user(user_id)


@router.get("/", response_model=list[UserResponse])
def list_users(controller: UserController = Depends(get_user_controller)):
    return controller.list_users()


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, data: UserUpdate, controller: UserController = Depends(get_user_controller)):
    return controller.update_user(user_id, data)


@router.delete("/{user_id}")
def delete_user(user_id: int, controller: UserController = Depends(get_user_controller)):
    return controller.delete_user(user_id)
