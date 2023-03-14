from . import router
from crud import EmailConfirmationCode, UserCRUD, ResponseException
from depends import Depends, Session, get_db
from pydantic import BaseModel, Field
from crud.exceptions import *
from utils import throws, HTTPResponseModel


class ResetPasswordArguments(BaseModel):
    password: str = Field(title='Новый пароль')
    confirm_password: str = Field(title='Подтверждение пароля')
    code: EmailConfirmationCode


resp = HTTPResponseModel.success('Пароль успешно изменён')


@router.post('/confirm_reset_password',
             summary='Подтверждение смены пароля',
             responses={
                 **throws.docs([
                     resp,
                     UserCRUD.confirm_password_reset,
                     WrongPasswordsDontMatchException,
                 ])
             })
def confirm_reset_password(data: ResetPasswordArguments,
                           db: Session = Depends(get_db)):
    try:
        ctx = UserCRUD.ctx()
        user = UserCRUD.handled(ctx).get(db, email=data.code.email)
        if ctx.has():
            raise WrongConfirmationCodeException()
        if data.password != data.confirm_password:
            raise WrongPasswordsDontMatchException()
        UserCRUD.confirm_password_reset(user, data.code, data.password)
        return resp.response()
    except ResponseException as e:
        raise e.get()
