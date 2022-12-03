from pydantic import BaseModel, Field
from config import Config
class HTTPResponseModel(BaseModel):
    details: str = Field(..., title='Детали ответа')

class TokenModel(BaseModel):
    access_token: str = Field(..., title='Токен доступа')
    expire: int | None = Field(Config.Settings.TOKEN_EXPIRE_INTERVAL, title='Время жизни токена')
