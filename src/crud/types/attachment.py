import re
from config import Config
from .base import AbstractTypeBase
from pydantic import AnyHttpUrl

_DEFAULT = 'DEFAULT'
_attachment_regex = re.compile(r'^[0-9A-Za-z]{16}$|^%s$' % (_DEFAULT,))
class AttachmentID(str, AbstractTypeBase):
    @classmethod
    def default(cls):
        return _DEFAULT
    @classmethod
    def example_url(cls):
        return cls(cls.default()).url()

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern=_attachment_regex.pattern,
            title='Вложение (ID изображения)'
        )

    @classmethod
    def validate(cls, v):
        if v is None or v == cls.default():
            return cls.default()
        if not isinstance(v, str):
            raise TypeError('string required')
        if not _attachment_regex.match(v):
            raise TypeError('Invalid attachment id format')
        return cls(v)

    def url(self):
        return f'{Config.AttachmentsService.PUBLIC_URL}{super().__str__()}.jpg'

    def __str__(self):
        return self

    def __repr__(self):
        return f'<{self.__class__.__name__} ({super().__str__()})>'
class AttachmentURL(AttachmentID):
    @classmethod
    def __modify_schema__(cls, field_schema):
        super().__modify_schema__(field_schema)
        field_schema.update(
            pattern=None,
            example=cls.example_url(),
        )
    def __str__(self):
        return self.url()

class AttachmentUploadURL(AnyHttpUrl):
    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        super().__modify_schema__(field_schema)
        field_schema.update(
            title='Ссылка для загрузки вложения',
            example=f'{Config.AttachmentsService.PUBLIC_URL}/upload/AAAAAAA'
        )

