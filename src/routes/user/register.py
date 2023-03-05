from utils import HTTPResponseModel
from . import router
from fastapi import Request
from depends import get_db, Session, Depends, get_mail, MailManager
from config import Config
from utils.throws import throws
from crud import (
    UserRegistrationForm,
    UserCRUD,
    UserPublic,
    UserAlreadyExistsException,
    UserNotFoundException,
    UserNotActiveException,
    cv,
)
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
             UserCRUD.generate_confirmation_code,
             UserNotFoundException,
             UserAlreadyExistsException,
             UserNotActiveException,
             resp,
         ]),
     }
)
def register(request: Request,
             data: UserRegistrationForm,
             db: Session = Depends(get_db),
             mail: MailManager = Depends(get_mail)):
    try:
        user = UserCRUD.register(db, data, not Config.Email.ENABLED)
        if Config.Email.ENABLED:
            code = UserCRUD.generate_confirmation_code(db, user.id, cv.REGISTRATION)
            confirm_link = request.url_for('confirm_email', code=code)
            mail.send_confirmation(user.email, confirm_link, user)
        return resp.response()
    except UserAlreadyExistsException:
        ctx = UserCRUD.ctx()
        user = UserCRUD.handled(ctx).get_user_by_registration_data(db, data)
        if ctx.has(UserNotFoundException):
            raise UserNotFoundException.get()
        if user.is_active:
            raise UserAlreadyExistsException.get()
        raise UserNotActiveException.get()




