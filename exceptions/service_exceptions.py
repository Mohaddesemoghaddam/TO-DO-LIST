from .base import AppException, ValidationError

class ServiceError(AppException):
    pass

class ProjectValidationError(ValidationError):
    pass

class TaskValidationError(ValidationError):
    pass

