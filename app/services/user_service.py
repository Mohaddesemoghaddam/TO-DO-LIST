from sqlalchemy.orm import Session
from models.user import User
from app.repositories.user_repository import UserRepository



class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def create_user(self, username: str, full_name: str, email: str):
        # check username duplicate
        if self.repo.get_by_username(username):
            raise Exception("Username already exists")

        # check email duplicate
        if self.repo.get_by_email(email):
            raise Exception("Email already registered")

        user = User(
            username=username,
            full_name=full_name,
            email=email
        )

        return self.repo.create(user)

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip, limit)

    def update_user(self, user_id: int, data: dict):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # duplicate username if changed
        if "username" in data:
            existing = self.repo.get_by_username(data["username"])
            if existing and existing.id != user_id:
                raise Exception("Username already exists")

        # duplicate email if changed
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
