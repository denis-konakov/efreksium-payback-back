from fastapi import BackgroundTasks
from mail import MailManager
from utils.throws import throws

@throws
def get_mail(bt: BackgroundTasks) -> MailManager:
    return MailManager(background_tasks=bt)

__all__ = (
    'get_mail',
    'MailManager'
)
