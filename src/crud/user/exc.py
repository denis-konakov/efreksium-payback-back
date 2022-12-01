class AuthorizationException(Exception):
    pass

class UserAlreadyExistsException(AuthorizationException):
    pass

class UserNotFoundException(AuthorizationException):
    pass

class WrongPasswordException(AuthorizationException, ValueError):
    pass

class InvalidTokenException(AuthorizationException, ValueError):
    pass

class TokenExpiredException(InvalidTokenException):
    pass

