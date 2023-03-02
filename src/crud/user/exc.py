from utils.response import ResponseException
class AuthorizationException(ResponseException):
    pass

class UserNotActiveException(AuthorizationException):
    META = dict(status_code=403, details='Пользователь не активирован')

class WrongConfirmationCodeException(AuthorizationException, ValueError):
    META = dict(status_code=400, details='Некорректный код подтверждения')

class UserAlreadyExistsException(AuthorizationException):
    META = dict(status_code=400, details='Пользователь с такими данными уже существует')

class UserNotFoundException(AuthorizationException):
    META = dict(status_code=404, details='Пользователь с такими данными не найден')

class WrongPasswordException(AuthorizationException, ValueError):
    META = dict(status_code=401, details='Некорректный логин или пароль')

class WrongConfirmationVariant(AuthorizationException):
    META = dict(status_code=401, details='Ошибка состояния кода подтверждения')

class InvalidTokenException(AuthorizationException, ValueError):
    META = dict(status_code=401, details='Некорректный токен доступа')

class TokenDecodeException(InvalidTokenException):
    pass
class TokenExpiredException(InvalidTokenException):
    pass

