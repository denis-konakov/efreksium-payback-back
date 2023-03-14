import re
from .base import AbstractTypeBase
_phone_regex = re.compile(r'^(\+7|8)?[0-9]{10}$')

class PhoneNumber(str, AbstractTypeBase):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=_phone_regex.pattern,
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not _phone_regex.match(v):
            raise TypeError('Invalid phone format')
        return cls(v)

    def __repr__(self):
        return f'<{self.__class__.__name__} ({self})>'
        
