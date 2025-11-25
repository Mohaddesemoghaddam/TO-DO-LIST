from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model

    def add(self, instance: ModelType):
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance

    def get(self, id: int) -> ModelType | None:
        return self.session.get(self.model, id)

    def get_all(self):
        return self.session.query(self.model).all()

    def delete(self, id: int) -> bool:
        instance = self.get(id)
        if not instance:
            return False
        self.session.delete(instance)
        self.session.commit()
        return True
