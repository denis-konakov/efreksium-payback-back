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
@router.post(
    '/register',
     summary='Регистрация пользователя',
     responses={
         **throws.docs([
             UserCRUD.register,
             UserCRUD.generate_confirmation_code,
             UserNotFoundException,
             UserAlreadyExistsException,
             UserNotActiveException
         ]),
         200: {
             'description': 'Регистрация прошла успешно',
             'model': UserPublic
         },
     }
)
def register(request: Request,
             data: UserRegistrationForm,
             db: Session = Depends(get_db),
             mail: MailManager = Depends(get_mail)) -> UserPublic:
    try:
        user = UserCRUD.register(db, data, not Config.Email.ENABLED)
        if Config.Email.ENABLED:
            code = UserCRUD.generate_confirmation_code(db, user.id, cv.REGISTRATION)
            confirm_link = request.url_for('confirm_user', code=code)
            mail.send_confirmation(user.email, confirm_link, user)
        return UserPublic.from_orm(user)
    except UserAlreadyExistsException:
        ctx = UserCRUD.ctx()
        user = UserCRUD.handled(ctx).get_user_by_registration_data(db, data)
        if ctx.has(UserNotFoundException):
            raise UserNotFoundException.get()
        if user.is_active:
            raise UserAlreadyExistsException.get()
        raise UserNotActiveException.get()




