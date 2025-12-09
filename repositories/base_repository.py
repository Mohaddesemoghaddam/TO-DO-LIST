# from sqlalchemy.orm import Session
# from typing import Generic, TypeVar, Type

# T = TypeVar("T")


# class BaseRepository(Generic[T]):
#     def __init__(self, model: Type[T], db: Session):
#         self.model = model
#         self.db = db

#     def get_all(self):
#         return self.db.query(self.model).all()

#     def get_by_id(self, id: int):
#         return self.db.query(self.model).filter(self.model.id == id).first()

#     def create(self, **kwargs):
#         obj = self.model(**kwargs)
#         self.db.add(obj)
#         self.db.commit()
#         self.db.refresh(obj)
#         return obj

#     def delete(self, obj):
#        self.db.delete(obj)
#        self.db.commit()
#        return True


#     def update(self, obj, **kwargs):
#         for key, value in kwargs.items():
#             setattr(obj, key, value)
#         self.db.commit()
#         self.db.refresh(obj)
#         return obj
from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(Generic[T]):
    """
    Generic repository class for managing basic CRUD operations.

    Acts as a reusable foundation for all entity repositories.
    It encapsulates session handling and basic persistence operations.
    """

    def __init__(self, model: Type[T], db: Session):
        """
        Initialize the repository with a SQLAlchemy model and a database session.
        """
        self.model = model
        self.db = db

    # ----------------------------------------------------
    # READ OPERATIONS
    # ----------------------------------------------------
    def get_all(self) -> List[T]:
        """
        Retrieve all records of the model from the database.
        """
        return self.db.query(self.model).all()

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Retrieve a single record by its ID.
        """
        return (
            self.db.query(self.model)
            .filter(self.model.id == id)
            .first()
        )

    # ----------------------------------------------------
    # CREATE
    # ----------------------------------------------------
    def create(self, **kwargs) -> T:
        """
        Create and persist a new record in the database.

        Returns the created object after commit & refresh.
        """
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # ----------------------------------------------------
    # UPDATE
    # ----------------------------------------------------
    def update(self, obj: T, **kwargs) -> T:
        """
        Update a record’s attributes and persist changes to the database.
        """
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    # ----------------------------------------------------
    # DELETE
    # ----------------------------------------------------
    def delete(self, obj: T) -> bool:
        """
        Delete a record from the database.

        Returns True after successful deletion.
        """
        self.db.delete(obj)
        self.db.commit()
        return True
