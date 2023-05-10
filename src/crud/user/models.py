from pydantic import BaseModel, EmailStr, Field, validator
from ..subscription.models import SubscriptionVariant
from ..types import PhoneNumber, Username, AttachmentID

class UserShared(BaseModel):
    id: int = Field(title='Идентификатор пользователя')
    username: Username = Field(title='Имя пользователя')
    avatar: AttachmentID = Field(title='Аватар пользователя')
    class Config:
        orm_mode = True

class UserPublic(UserShared):
    email: EmailStr = Field(title='Электронная почта')
    number: PhoneNumber = Field(title='Номер телефона')
    email_confirmed: bool = Field(title='Активирована ли почта пользователя')
    subscription: SubscriptionVariant | None = Field(title='Информация о подписке')
    class Config:
        orm_mode = True

class UserPublicWithGroupsAndFriends(UserPublic):
    groups: 'list[GroupFull]'
    friends: list[UserShared]
    class Config:
        orm_mode = True


class UserPrivate(UserPublicWithGroupsAndFriends):
    hashed_password: str = Field(title='Хэш пароля')
    email_confirmation_code: str = Field(title='Хеш кода подтверждения')
    password_reset_code: str = Field(title='Хеш кода подтверждения для смены пароля')
    class Config:
        orm_mode = True

class UserAuthorizationForm(BaseModel):
    email: EmailStr = Field(title='Почта пользователя')
    password: str = Field(title='Пароль')

class UserRegistrationForm(BaseModel):
    username: Username = Field(title='Имя пользователя')
    email: EmailStr = Field(title='Электронная почта')
    number: PhoneNumber = Field(title='Номер телефона')
    password: str = Field(title='Пароль')

