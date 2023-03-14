from fastapi import BackgroundTasks
from mail import MailManager
from utils.throws import throws
from crud.exceptions import ResponseException
from jinja2.exceptions import TemplateError
@throws([

])
def get_mail(bt: BackgroundTasks) -> MailManager:
    try:
        yield MailManager(background_tasks=bt)
    except TemplateError:
        raise ResponseException().get()
__all__ = (
    'get_mail',
    'MailManager'
)
