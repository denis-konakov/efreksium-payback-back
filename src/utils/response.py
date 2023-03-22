from pydantic import BaseModel, Field
from config import Config
from typing import Callable, TypeVar, Generic
from fastapi import HTTPException
from pydantic.generics import GenericModel


T = TypeVar('T')
class HTTPResponseDetail(GenericModel, Generic[T]):
    response: T = Field(title='Данные ответа')
    detail: str = Field(title='Текстовый код ответа')
    program_code: str = Field(title='Программный код ответа')
    status: bool = Field(title='Статус выполнения запроса')

class HTTPResponseModel(GenericModel, Generic[T]):
    detail: HTTPResponseDetail[T] = Field(title='Детали ответа')
    @classmethod
    def success(cls, detail: str, response: type = None, *, program_code: str = 'success') -> 'type[ResponseException]':
        class SuccessResponse(ResponseException):
            META = dict(
                status_code=200,
                program_code=program_code,
                detail=detail,
                status=True,
                response=response
            )
        return SuccessResponse
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
T2 = TypeVar('T2')
class ResponseException(Exception, Generic[T2]):
    META: MetaDataDictType = dict(
        status_code=500,
        detail='Internal server error',
        program_code=lambda cls: _camel_to_snake(_search_parent_has_meta(cls).__name__),
        status=False,
    )
    @classmethod
    def get_meta(cls, **kwargs: MetaDataDictType) -> dict[str, str | int]:
        parents = reversed([i for i in cls.__mro__ if issubclass(i, ResponseException)])
        meta = {}
        for i in parents:
            meta.update(i.META)
        meta.update(kwargs)
        for i in meta.keys():
            if callable(meta.get(i)) and meta.get(i).__class__.__name__ == 'function':
                meta[i] = meta[i](cls)
        return meta
    @classmethod
    def status_code(cls) -> int:
        return int(cls.get_meta().get('status_code', 500))
    @classmethod
    def detail(cls):
        return cls.get_meta().get('detail', '')
    @classmethod
    def program_code(cls):
        return cls.get_meta().get('program_code', '')

    @classmethod
    def status(cls):
        return cls.get_meta().get('status', False)
    @classmethod
    def get(cls, **kwargs: MetaDataDictType):
        return HTTPException(
            status_code=cls.status_code(),
            detail=cls.get_meta(**kwargs)
        )
    @classmethod
    def response(cls, response: T2 = None, **kwargs: MetaDataDictType) -> HTTPResponseModel[T2] | T2:
        return HTTPResponseModel[T2](**{
            'detail': cls.get_meta(**{**kwargs, 'response': response}),
        })
    @classmethod
    def example(cls):
        return {
            'summary': cls.detail(),
            'value': {
                'detail': {
                    'detail': cls.detail(),
                    'program_code': cls.program_code(),
                    'status': cls.status(),
                    'response': None
                }
            }
        }
    @classmethod
    def raise_(cls, **kwargs):
        raise cls.get(**kwargs)

