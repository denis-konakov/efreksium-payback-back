from pydantic import BaseModel, EmailStr
from ..subscription.models import Subscription
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    number: str
    is_active: bool
    subscription_id: int
    subscription: Subscription
    class Config:
        orm_mode = True
class UserPrivate(UserPublic):
    hashed_password: str
    class Config:
        orm_mode = True

class UserAuthorizationData(BaseModel):
    username: str
    password: str

class UserRegistrationData(BaseModel):
    username: str
    email: EmailStr
    number: str
    password: str
