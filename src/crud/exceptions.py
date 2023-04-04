from utils.response import ResponseException

# Config

class WrongConfigurationException(ResponseException):
    META = dict(status_code=500, detail='Ошибка конфигурации')


# Authorization
class AuthorizationException(ResponseException):
    META = dict(status_code=401)

class UserNotActiveException(AuthorizationException):
    META = dict(detail='Пользователь не активирован')

class WrongConfirmationCodeException(AuthorizationException, ValueError):
    META = dict(detail='Некорректный код подтверждения')

class UserAlreadyExistsException(AuthorizationException):
    META = dict(detail='Пользователь с такими данными уже существует')

class UserNotFoundException(AuthorizationException):
    META = dict(status_code=404, detail='Пользователь с такими данными не найден')

class WrongPasswordException(AuthorizationException, ValueError):
    META = dict(detail='Некорректный логин или пароль')

class WrongPasswordsDontMatchException(WrongPasswordException):
    META = dict(detail='Введенные пароли не совпадают')

class InvalidTokenException(AuthorizationException, ValueError):
    META = dict(detail='Некорректный токен доступа')

class TokenDecodeException(InvalidTokenException):
    pass
class TokenExpiredException(InvalidTokenException):
    pass
# Email

class EmailSendMessageException(ResponseException):
    META = dict(detail='Ошибка отправки письма')

# Friends
class FriendException(ResponseException):
    META = dict(status_code=401)

class AddFriendException(ResponseException):
    META = dict(detail='Ошибка при добавлении пользователя в друзья')

class CannotAddHimselfToFriendsException(AddFriendException):
    META = dict(detail='Нельзя добавить себя в друзья')

class UserAlreadyYourFriendException(AddFriendException):
    META = dict(detail='Этот пользователь уже у вас в друзьях')

# Attachments

class AttachmentsException(ResponseException):
    META = dict(status_code=401, detail='Ошибка взаимодействия с вложениями')

class AttachmentServiceDeniedException(AttachmentsException):
    META = dict(detail='Ошибка взаимодействия с сервисом вложений')

class AvatarAlreadyExistsException(AttachmentsException):
    META = dict(detail='У вас уже есть аватар')


# Groups

class GroupsException(ResponseException):
    META = dict(status_code=401, detail='Ошибка модуля групп')

class GroupsCreateLimitException(GroupsException):
    META = dict(detail='Превышен лимит создания групп')

class UserAlreadyInGroupException(ResponseException):
    META = dict(detail='Пользователь уже находится в этой группе')
