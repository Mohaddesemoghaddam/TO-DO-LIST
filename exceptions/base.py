class AppException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class NotFoundError(AppException):
    pass


class ValidationError(AppException):
    pass


