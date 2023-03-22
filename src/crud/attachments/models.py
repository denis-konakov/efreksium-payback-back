from pydantic import BaseModel, Field, AnyHttpUrl
from crud.types import AttachmentUploadURL, AttachmentID
class AvatarUploadInfo(BaseModel):
    url: AttachmentUploadURL = Field(title='Ссылка для загрузки изображения')
    image_id: AttachmentID = Field(title='ID изображения')
    key: str = Field(title='Секретный ключ для загрузки изображения', example='b4d508cb4d4d82d2f6b685575551d6f4')
    class Config:
        orm_mode = True
