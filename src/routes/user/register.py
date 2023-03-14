from utils import HTTPResponseModel
from . import router
from fastapi import Request
from depends import get_db, Session, Depends, get_mail, MailManager
from config import Config
from depends import confirm
from utils import throws, url_add_arguments
from crud import (
    UserRegistrationForm,
    UserCRUD,
    UserPublic,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
)
from pydantic import AnyHttpUrl
from config import Config
resp = HTTPResponseModel.success(
    'Код подтверждения почты отправлен' if Config.Email.ENABLED else
    'Успешная регистрация'
)

@router.post(
    '/register',
     summary='Регистрация пользователя',
     responses={
         **throws.docs([
             UserCRUD.register,
             UserCRUD.generate_email_confirmation_code,
             UserNotFoundException,
             UserAlreadyExistsException,
             UserNotActiveException,
             resp,
         ]),
     }
)
def register(data: UserRegistrationForm,
             link: confirm.type = Depends(confirm),
             db: Session = Depends(get_db),
             mail: MailManager = Depends(get_mail)):
    try:
        user = UserCRUD.register(db, data, not Config.Email.ENABLED)
        if Config.Email.ENABLED:
            code = UserCRUD.generate_email_confirmation_code(user)
            mail.send_confirmation(user.email, link(code.private), user)
        return resp.response()
    except UserAlreadyExistsException:
        ctx = UserCRUD.ctx()
        user = UserCRUD.handled(ctx).get(db, email=data.email)
        if ctx.has(UserNotFoundException):
            raise UserNotFoundException.get()
        if user.email_confirmed:
            raise UserAlreadyExistsException.get()
        raise UserNotActiveException.get()




