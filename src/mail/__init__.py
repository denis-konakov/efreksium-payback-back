from fastapi_mail import ConnectionConfig, MessageSchema, MessageType, FastMail
from config import Config
from pathlib import Path
from fastapi import BackgroundTasks
from loguru import logger

from crud import UserPublic

path = Path(Config.Email.TEMPLATES_DIR)
assert path.exists(), f'Path {path} does not exist'
assert path.is_dir(), f'Path {path} is not a directory'


conf = ConnectionConfig(
    MAIL_USERNAME=Config.Email.FROM_NAME,
    MAIL_PASSWORD=Config.Email.PASSWORD,
    MAIL_FROM=Config.Email.FROM,
    MAIL_PORT=Config.Email.PORT,
    MAIL_SERVER=Config.Email.SERVER,
    TEMPLATE_FOLDER=path,
    MAIL_STARTTLS=Config.Email.TLS,
    MAIL_SSL_TLS=Config.Email.SSL_TLS,
)

class MailManager:
    def __init__(self, background_tasks: BackgroundTasks):
        self.__bt: BackgroundTasks = background_tasks

    def send(self,
             to: str,
             subject: str,
             template: str,
             context: dict):
        msg = MessageSchema(
            subject=subject,
            recipients=[to],
            template_body=context,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        self.__bt.add_task(
            fm.send_message,
            msg,
            template
        )
    def send_confirmation(self, to: str, link: str, user: UserPublic):
        self.send(
            to,
            'Подтверждение почты',
            'confirm_email.html',
            {
                'confirm_link': link,
                'user': user
            }
        )








