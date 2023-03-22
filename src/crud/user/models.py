from pydantic import BaseModel, EmailStr, Field, validator
from ..subscription.models import SubscriptionInfo
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
    subscription_id: int | None = Field(title='Идентификатор подписки')
    subscription: SubscriptionInfo | None = Field(title='Информация о подписке')
    class Config:
        orm_mode = True

class UserPrivate(UserPublic):
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

