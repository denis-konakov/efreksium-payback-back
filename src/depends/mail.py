from fastapi import BackgroundTasks
from mail import MailManager
from utils.throws import throws
from crud.exceptions import EmailSendMessageException
@throws([
    EmailSendMessageException
])
def get_mail(bt: BackgroundTasks) -> MailManager:
    yield MailManager(background_tasks=bt)

__all__ = (
    'get_mail',
    'MailManager'
)
