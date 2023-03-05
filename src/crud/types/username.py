import re

_username_regex = re.compile(r'^[a-zA-Zа-яА-Я0-9 _-]$')


class Username(str):
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
