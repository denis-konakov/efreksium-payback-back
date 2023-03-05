from fastapi import Request

from . import router
from depends import Session, get_db, Depends, get_mail, MailManager, get_confirm_link, get_confirm_link_type
from crud import UserCRUD, UserNotFoundException, WrongPasswordException, UserAlreadyExistsException
from pydantic import EmailStr
from utils.response import HTTPResponseModel
from utils.throws import throws

resp = HTTPResponseModel.success('Код подтверждения почты отправлен')

@router.post(
    '/send_registration_confirm_code',
    summary='Отправка кода подтверждения почты',
    responses={
        **throws.docs([
            UserNotFoundException,
            WrongPasswordException,
            UserAlreadyExistsException,
            UserCRUD.generate_confirmation_code,
            resp
        ]),
    }
)
def send_registration_confirm_code(email: EmailStr,
                                   confirm_link: get_confirm_link_type = Depends(get_confirm_link),
                                   db: Session = Depends(get_db),
                                   mail: MailManager = Depends(get_mail)):
    ctx = UserCRUD.ctx()
    user = UserCRUD.handled(ctx).get_user_by_email(db, email)
    if ctx.has(UserNotFoundException):
        raise UserNotFoundException.get()
    if user.is_active:
        raise UserAlreadyExistsException.get()
    code = UserCRUD.generate_confirmation_code(db, user.id, UserCRUD.cv.REGISTRATION)
    link = confirm_link(code)
    mail.send_confirmation(user.email, link, user)
    return resp.response()


