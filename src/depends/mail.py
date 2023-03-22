from fastapi import BackgroundTasks
from mail import MailManager
from utils.throws import throws
from crud.exceptions import EmailSendMessageException
from loguru import logger
@throws([
    EmailSendMessageException
])
def get_mail(bt: BackgroundTasks) -> MailManager:
    try:
        yield MailManager(background_tasks=bt)
    except Exception as e:
        logger.error('email interaction exception: {}', e)
        raise EmailSendMessageException.get()
__all__ = (
    'get_mail',
    'MailManager'
)
