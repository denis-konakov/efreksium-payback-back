import re
from .base import AbstractTypeBase
_username_regex = re.compile(r'^[a-zA-Zа-яА-Я0-9 _-]{3,32}$')


class Username(str, AbstractTypeBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=_username_regex.pattern,
            example='Иван Иванов'
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not _username_regex.match(v):
            raise TypeError('Invalid username')
        return cls(v)

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self})>'
