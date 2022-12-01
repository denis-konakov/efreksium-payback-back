from pydantic import BaseModel
from datetime import datetime
class SubscriptionVariant(BaseModel):
    id: int
    name: str
    description: str
    price: int
    duration: int
    class Config:
        orm_mode = True

class Subscription(BaseModel):
    id: int
    variant_id: int
    variant: SubscriptionVariant
    receipt_time: datetime
    expiration_time: datetime
    users: 'list[UserPublic]'
    class Config:
        orm_mode = True
