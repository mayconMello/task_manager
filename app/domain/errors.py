class BaseError(Exception):
    default_message = 'An unknown error occurred.'

    def __init__(self, message: str = None):
        self.message = message or self.default_message

        super().__init__(self.message)


class ResourceNotFoundError(BaseError):
    default_message = 'Resource not found'


class UserAlreadyExists(BaseError):
    default_message = 'User already exists.'


class InvalidCredentialsError(BaseError):
    default_message = 'Invalid credentials.'


class MaxFileSizeError(BaseError):
    default_message = 'Maximum file size is exceeded.'



class OperationNotAllowedError(BaseError):
    default_message = 'Operation not allowed.'