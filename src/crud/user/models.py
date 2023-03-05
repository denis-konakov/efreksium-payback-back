from pydantic import BaseModel, EmailStr, Field, validator
from ..subscription.models import SubscriptionInfo
from ..types import PhoneNumber, Username
from crud.db_models.user import ConfirmationVariant

class UserShared(BaseModel):
    id: int = Field(title='Идентификатор пользователя')
    username: Username = Field(title='Имя пользователя')

class UserPublic(UserShared):
    email: EmailStr = Field(title='Электронная почта')
    number: PhoneNumber = Field(title='Номер телефона')
    is_active: bool = Field(title='Активирована ли почта пользователя')
    subscription_id: int | None = Field(title='Идентификатор подписки')
    subscription: SubscriptionInfo | None = Field(title='Информация о подписке')
    class Config:
        orm_mode = True

class UserPrivate(UserPublic):
    hashed_password: str = Field(title='Хэш пароля')
    confirmation_code: str = Field(title='Хеш кода подтверждения')
    confirmation_variant: ConfirmationVariant = Field(title='Вариант подтверждения почты')
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

