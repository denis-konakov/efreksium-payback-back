from pydantic.generics import GenericModel
from pydantic import Field, BaseModel
from typing import Generic, TypeVar
T = TypeVar('T')


class PaginateContent(GenericModel, Generic[T]):
    result: list[T] = Field(title='Полученные данные')
    count: int = Field(title='Количество записей в результате выборки')
    total: int = Field(title='Общее количество записей в базе')
    class Config:
        arbitrary_types_allowed = True

class PaginateContentParams(BaseModel):
    offset: int = Field(title='Смещение выборки', ge=0)
    count: int = Field(title='Максимальное количество записей в результате', ge=10, le=100)
