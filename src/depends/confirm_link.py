from utils import throws
from enum import StrEnum
from fastapi import Request, Depends, Query
from pydantic import AnyHttpUrl
from utils import url_add_arguments
from crud import PublicPrivateCodePair
from typing import Callable

class ConfirmLinkVariant(StrEnum):
    CONFIRM_EMAIL = 'confirm_email'
    RESET_PASSWORD = 'reset_password'


class ConfirmLink:
    def __init__(self):
        self.type = Callable[[str | PublicPrivateCodePair], str]
    def __call__(self, redirect: AnyHttpUrl = Query(title='Ссылка для перенаправления авторизации')):
        def confirm_link_wrapper(code: str | PublicPrivateCodePair) -> str:
            if isinstance(code, PublicPrivateCodePair):
                code = code.private
            return url_add_arguments(redirect, {
                'confirm_code': code
            })
        return confirm_link_wrapper

confirm: ConfirmLink = throws(ConfirmLink())
