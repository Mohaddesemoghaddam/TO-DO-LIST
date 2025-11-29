from sqlalchemy.orm import Session
from models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user.user_create import UserCreate
from app.schemas.user.user_update import UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def create_user(self, user_data: UserCreate):
        # username duplicate
        if self.repo.get_by_username(user_data.username):
            raise Exception("Username already exists")

        # email duplicate
        if self.repo.get_by_email(user_data.email):
            raise Exception("Email already registered")

        user = User(
            username=user_data.username,
            full_name=user_data.full_name,
            email=user_data.email
        )

        return self.repo.create(user)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def update_user(self, user_id: int, update_data: UserUpdate):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")

        data = update_data.dict(exclude_unset=True)

        # username duplicate
        if "username" in data:
            existing = self.repo.get_by_username(data["username"])
            if existing and existing.id != user_id:
                raise Exception("Username already exists")

        # email duplicate
        if "email" in data:
            existing = self.repo.get_by_email(data["email"])
            if existing and existing.id != user_id:
                raise Exception("Email already registered")

        return self.repo.update(user, data)

    def delete_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        self.repo.delete(user)
        return True
