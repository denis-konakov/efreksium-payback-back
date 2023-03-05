from pydantic import BaseModel, Field
from .. import UserPrivate, UserShared

class FriendPublic(BaseModel):
    id: int = Field(title='Идентификатор приглашения')
    sender_id: int = Field(title='Идентификатор отправителя приглашения')
    recipient_id: int = Field(title='Идентификатор получателя приглашения')
    sender: UserShared = Field(title='Отправитель приглашения')
    recipient: UserShared = Field(title='Получатель приглашения')
    status: bool = Field(title='Статус подтверждения приглашения')
    class Config:
        orm_mode = True

class FriendPrivate(FriendPublic):
    sender: UserPrivate = Field(title='Отправитель приглашения')
    recipient: UserPrivate = Field(title='Получатель приглашения')
    class Config:
        orm_mode = True
