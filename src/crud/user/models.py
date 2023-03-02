from pydantic import BaseModel, EmailStr, Field, validator
from ..subscription.models import SubscriptionInfo
from ..types import PhoneNumber
import re
class UserPublic(BaseModel):
    id: int = Field(title='Идентификатор пользователя')
    username: str = Field(title='Имя пользователя')
    email: EmailStr = Field(title='Электронная почта')
    number: PhoneNumber = Field(title='Номер телефона')
    is_active: bool = Field(title='Активирована ли почта пользователя')
    subscription_id: int | None = Field(title='Идентификатор подписки')
    subscription: SubscriptionInfo | None = Field(title='Информация о подписке')
    class Config:
        orm_mode = True
class UserPrivate(UserPublic):
    hashed_password: str = Field(title='Хэш пароля')
    class Config:
        orm_mode = True

class UserAuthorizationForm(BaseModel):
    email: EmailStr = Field(title='Почта пользователя')
    password: str = Field(title='Пароль')

class UserRegistrationForm(BaseModel):
    username: str = Field(title='Имя пользователя')
    email: EmailStr = Field(title='Электронная почта')
    number: PhoneNumber = Field(title='Номер телефона')
    password: str = Field(title='Пароль')
    @classmethod
    @validator('username')
    def check_username(cls, username):
        if not (3 < len(username) < 32):
            raise ValueError('Username must be at least 3 characters long and no more than 32')
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValueError('Username must contain only letters and numbers')
        return username

