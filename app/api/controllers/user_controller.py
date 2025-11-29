from fastapi import HTTPException, status
from app.services.user_service import UserService
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_update import UserUpdate
from app.schemas.user.user_response import UserResponse


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, data: UserCreate) -> UserResponse:
        user = self.user_service.create_user(data)
        return UserResponse.from_orm(user)

    def get_user(self, user_id: int) -> UserResponse:
        user = self.user_service.get_user(user_id)   # اصلاح نام متد
        return UserResponse.from_orm(user)

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.user_service.update_user(user_id, data)
        return UserResponse.from_orm(user)

    def delete_user(self, user_id: int) -> dict:
        self.user_service.delete_user(user_id)
        return {"message": "User deleted successfully"}

    def list_users(self) -> list[UserResponse]:
        users = self.user_service.list_users()   # اصلاح نام متد
        return [UserResponse.from_orm(u) for u in users]

