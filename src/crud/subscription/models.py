from pydantic import BaseModel, Field
from datetime import datetime
class SubscriptionVariant(BaseModel):
    id: int = Field(..., description='Идентификатор варианта подписки')
    name: str = Field(..., description='Название варианта подписки')
    description: str = Field(..., description='Описание варианта подписки')
    price: int = Field(..., description='Цена варианта подписки')
    duration: int = Field(..., description='Продолжительность варианта подписки в днях')
    class Config:
        orm_mode = True

class SubscriptionInfo(BaseModel):
    id: int = Field(..., description='Идентификатор подписки')
    variant_id: int = Field(..., description='Идентификатор варианта подписки')
    variant: SubscriptionVariant = Field(..., description='Информация о варианте подписки')
    receipt_time: datetime = Field(..., description='Время покупки подписки')
    expiration_time: datetime = Field(..., description='Время окончания подписки')
    class Config:
        orm_mode = True

class SubscriptionVariantFull(SubscriptionVariant):
    users: 'list[UserPublic]' = Field(..., description='Список пользователей с этой подпиской')
