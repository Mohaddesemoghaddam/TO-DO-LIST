from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

T = TypeVar("T")  # ORM model type

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    def get_all(self, db: Session):
        return db.query(self.model).all()

    def get_by_id(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def create(self, db: Session, obj: T):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    def delete(self, db: Session, id: int):
        obj = self.get_by_id(db, id)
        if obj is None:
            return None
        db.delete(obj)
        db.commit()
        return True
