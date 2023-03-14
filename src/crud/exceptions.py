from utils.response import ResponseException

# Authorization
class AuthorizationException(ResponseException):
    pass

class UserNotActiveException(AuthorizationException):
    META = dict(status_code=403, detail='Пользователь не активирован')

class WrongConfirmationCodeException(AuthorizationException, ValueError):
    META = dict(status_code=400, detail='Некорректный код подтверждения')

class UserAlreadyExistsException(AuthorizationException):
    META = dict(status_code=400, detail='Пользователь с такими данными уже существует')

class UserNotFoundException(AuthorizationException):
    META = dict(status_code=404, detail='Пользователь с такими данными не найден')

class WrongPasswordException(AuthorizationException, ValueError):
    META = dict(status_code=401, detail='Некорректный логин или пароль')

class WrongPasswordsDontMatchException(WrongPasswordException):
    META = dict(status_code=401, detail='Введенные пароли не совпадают')

class InvalidTokenException(AuthorizationException, ValueError):
    META = dict(status_code=401, detail='Некорректный токен доступа')

class TokenDecodeException(InvalidTokenException):
    pass
class TokenExpiredException(InvalidTokenException):
    pass

# Friends

class AddFriendException(ResponseException):
    META = dict(status_code=401, detail='Ошибка при добавлении пользователя в друзья')

class CannotAddHimselfToFriendsException(AddFriendException):
    META = dict(status_code=401, detail='Нельзя добавить себя в друзья')

class UserAlreadyYourFriendException(AddFriendException):
    META = dict(status_code=401, detail='Этот пользователь уже у вас в друзьях')
