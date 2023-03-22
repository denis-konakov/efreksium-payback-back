from config import Config
from crud import (
    UserRegistrationForm,
    UserCRUD,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
)
from depends import confirm
from depends import get_db, Session, Depends, get_mail, MailManager
from utils import HTTPResponseModel, ResponseException, throws
from . import router

resp = HTTPResponseModel.success(
    'Код подтверждения почты отправлен' if Config.Email.ENABLED else
    'Успешная регистрация'
)

@router.post(
    '/register',
     summary='Регистрация пользователя',
     responses={
         **throws.docs([
             confirm,
             get_db,
             get_mail,
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
    except ResponseException as e:
        raise e.get()





