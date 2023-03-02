from pydantic import BaseModel, Field
from config import Config
from typing import Callable
from fastapi import HTTPException


class HTTPResponseDetails(BaseModel):
    details: str = Field(..., title='Текстовый код ответа')
    program_code: str = Field(..., title='Программный код ответа')
class HTTPResponseModel(BaseModel):
    details: HTTPResponseDetails = Field(..., title='Детали ответа')
    @classmethod
    def success(cls, details: str) -> tuple[dict[int, dict], 'HTTPResponseModel']:
        return {200: {
            'description': f'{details} (Программный код success)',
            'model': HTTPResponseModel,
        }}, cls(details={
            'details': details,
            'program_code': 'success'
        })
class TokenModel(BaseModel):
    access_token: str = Field(..., title='Токен доступа')
    expire: int = Field(Config.Settings.TOKEN_EXPIRE_INTERVAL, title='Время жизни токена')


def _search_parent_has_meta(a: type) -> type:
    for i in a.__mro__:
        if 'META' in i.__dict__:
            return i
    raise ValueError('Parent with META field not found.')

def _camel_to_snake(s: str) -> str:
    s = list(s)
    for i, v in enumerate(s):
        if v.upper() == v:
            s[i] = '_' + v.lower()
    return ''.join(s)[1:]

MetaDataDictType = dict[str,
                        str |
                        int |
                        Callable[[type], str | int]
]
class ResponseException(Exception):
    BASE_META: MetaDataDictType = dict(
        status_code=500,
        details='Internal server error',
        program_code=lambda cls: _camel_to_snake(_search_parent_has_meta(cls).__name__)
    )
    META: MetaDataDictType = dict()
    @classmethod
    def get_meta(cls, **kwargs: MetaDataDictType) -> dict[str, str | int]:
        meta = {**cls.BASE_META, **cls.META, **kwargs}
        for i in meta.keys():
            if callable(meta.get(i)):
                meta[i] = meta[i](cls)
        return meta
    @classmethod
    def status_code(cls) -> int:
        return int(cls.get_meta().get('status_code', 500))
    @classmethod
    def details(cls):
        return cls.get_meta().get('details', '')
    @classmethod
    def program_code(cls):
        return cls.get_meta().get('program_code', '')
    @classmethod
    def get(cls, **kwargs: MetaDataDictType):
        return HTTPException(
            status_code=cls.status_code(),
            detail=cls.get_meta(**kwargs)
        )
    @classmethod
    def docs(cls):
        return {
            'description': f'{cls.details()} (Программный код: {cls.program_code()})',
            'model': HTTPResponseModel,
        }
    @classmethod
    def raise_(cls, **kwargs):
        raise cls.get(**kwargs)

