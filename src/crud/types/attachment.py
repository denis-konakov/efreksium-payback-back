import re
from config import Config
from .base import AbstractTypeBase
_attachment_regex = re.compile(r'^[0-9A-F]{16}$')


class Attachment(str, AbstractTypeBase):
    @classmethod
    def example(cls):
        return cls('default').url()
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            example=cls.example(),
            title='Вложение (ID изображения)'
        )
    @classmethod
    def validate(cls, v):
        if v is None or v == 'default':
            return cls.example()
        if not isinstance(v, str):
            raise TypeError('string required')
        if not _attachment_regex.match(v):
            raise TypeError('Invalid attachment id format')
        return cls(v)
    def url(self):
        return f'{Config.AttachmentsService.PUBLIC_URL}{super().__str__()}.jpg'

    def __str__(self):
        return self.url()

    def __repr__(self):
        return f'<{self.__class__.__name__} ({super().__str__()})>'

