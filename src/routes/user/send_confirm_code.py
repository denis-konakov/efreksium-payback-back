from fastapi import Request

from . import router
from depends import Session, get_db, Depends, get_mail, MailManager
from crud import UserCRUD, UserNotFoundException, WrongPasswordException, UserAlreadyExistsException
from pydantic import EmailStr
from utils.response import HTTPResponseModel
from utils.throws import throws

doc, resp = HTTPResponseModel.success('Код подтверждения почты отправлен')

@router.post(
    '/send_confirm_code',
    summary='Отправка кода подтверждения почты',
    responses={
        **throws.docs([
            UserNotFoundException,
            WrongPasswordException,
            UserAlreadyExistsException,
            UserCRUD.generate_confirmation_code
        ]),
        **doc,
    }
)
def send_confirm_code(email: EmailStr,
                      username: str,
                      request: Request,
                      db: Session = Depends(get_db),
                      mail: MailManager = Depends(get_mail)):
    ctx = UserCRUD.ctx()
    user = UserCRUD.handled(ctx).get_user_by_email(db, email)
    if ctx.has(UserNotFoundException):
        raise UserNotFoundException.get()
    if user.username != username:
        raise WrongPasswordException.get()
    if user.is_active:
        raise UserAlreadyExistsException.get()
    code = UserCRUD.generate_confirmation_code(db, user.id)
    confirm_link = request.url_for('confirm_user', code=code)
    mail.send_confirmation(user.email, confirm_link, user)
    return resp


