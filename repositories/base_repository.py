# from sqlalchemy.orm import Session
# from typing import Generic, TypeVar, Type

# T = TypeVar("T")  # ORM model type

# class BaseRepository(Generic[T]):
#     def __init__(self, model: Type[T]):
#         self.model = model

#     def get_all(self, db: Session):
#         return db.query(self.model).all()

#     def get_by_id(self, db: Session, id: int):
#         return db.query(self.model).filter(self.model.id == id).first()

#     def create(self, db: Session, **kwargs):
#         obj = self.model(**kwargs)
#         db.add(obj)
#         db.commit()
#         db.refresh(obj)
#         return obj


#     def delete(self, db: Session, id: int):
#         obj = self.get_by_id(db, id)
#         if obj is None:
#             return None
#         db.delete(obj)
#         db.commit()
#         return True
#     def update(self, db: Session, obj, **kwargs):
#         for key, value in kwargs.items():
#             setattr(obj, key, value)
#         db.commit()
#         db.refresh(obj)
#         return obj
# repositories/base_repository.py
from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: Session):
        self.model = model
        self.db = db

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, id: int):
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, obj):
       self.db.delete(obj)
       self.db.commit()
       return True


    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj
