from .base import AppException

class ServiceException(AppException):
    """Base class for all service layer exceptions."""
    pass


class ProjectNotFoundException(ServiceException):
    """Raised when a project is not found."""
    pass


class ProjectValidationError(ServiceException):
    """Raised when project data is invalid."""
    pass


class TaskNotFoundException(ServiceException):
    """Raised when a task is not found."""
    pass


class TaskValidationError(ServiceException):
    """Raised when task data is invalid."""
    pass
