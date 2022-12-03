from pydantic import BaseModel, EmailStr, Field
from ..subscription.models import SubscriptionInfo
class UserPublic(BaseModel):
    id: int = Field(..., title='Идентификатор пользователя')
    username: str = Field(..., title='Имя пользователя')
    email: EmailStr = Field(..., title='Электронная почта')
    number: str = Field(..., title='Номер телефона')
    is_active: bool = Field(..., title='Активирована ли почта пользователя')
    subscription_id: int | None = Field(..., title='Идентификатор подписки')
    subscription: SubscriptionInfo | None = Field(..., title='Информация о подписке')
    class Config:
        orm_mode = True
class UserPrivate(UserPublic):
    hashed_password: str = Field(..., title='Хэш пароля')
    class Config:
        orm_mode = True

class UserAuthorizationData(BaseModel):
    email: EmailStr = Field(..., title='Почта пользователя')
    password: str = Field(..., title='Пароль')

class UserRegistrationData(BaseModel):
    username: str = Field(..., title='Имя пользователя')
    email: EmailStr = Field(..., title='Электронная почта')
    number: str = Field(..., title='Номер телефона')
    password: str = Field(..., title='Пароль')
