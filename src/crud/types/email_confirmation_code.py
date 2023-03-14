from .base import AbstractTypeBase
import base64
from pydantic import EmailStr
from secrets import token_hex
from passlib.context import CryptContext
from dataclasses import dataclass

@dataclass
class PublicPrivateCodePair:
    public: str
    private: 'EmailConfirmationCode'

class EmailConfirmationCode(str, AbstractTypeBase):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise ValueError()
        cls._separate_confirm_code(v)
        return cls(v)
    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(
            title='Код подтверждения отправленный на почту',
            example='YWRtaW5AbWFpbC5ydTowMDExMjIzMzQ0NTU2Njc3ODg5OUFBQkJDQ0RERUVGRg=='
        )
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @property
    def email(self):
        return self._separate_confirm_code(self)[1]
    @property
    def secret(self):
        return self._separate_confirm_code(self)[0]
    @property
    def code(self):
        return self.secret

    def verify(self, pwd_context: CryptContext, public_code: str):
        print('check', self.secret, public_code)
        return pwd_context.verify(self.secret, public_code)

    @classmethod
    def _separate_confirm_code(cls, code: str) -> tuple[str, EmailStr]:
        code, email = base64.b64decode(code).decode().split(':')
        return code, email
    @classmethod
    def generate(cls, pwd_context: CryptContext, email: EmailStr) -> PublicPrivateCodePair:
        code = token_hex(16)

        scode = pwd_context.hash(code)
        print('generate', code, scode)
        code = base64.b64encode(f'{code}:{email}'.encode()).decode()
        return PublicPrivateCodePair(public=scode, private=EmailConfirmationCode(code))



