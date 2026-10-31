from .base import AppException, NotFoundError

class RepositoryError(AppException):
    pass

class ObjectNotFoundError(NotFoundError):
    pass

