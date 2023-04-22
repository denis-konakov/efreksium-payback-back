from pydantic import EmailStr

from . import router
from depends import get_db, Depends, Session
from crud import UserAuthorizationForm, UserCRUD, AuthorizationException, UserNotActiveException, WrongPasswordException
from utils.response import HTTPResponseModel, TokenModel
from utils.throws import throws
from fastapi.security import OAuth2PasswordRequestForm
from utils import cast
from crud.exceptions import *
resp = HTTPResponseModel.success('Авторизация прошла успешно', TokenModel)


@router.post('/login',
             summary='Авторизация пользователя в системе',
             responses={
                 **throws.docs([
                     UserCRUD.login,
                     UserCRUD.generate_token,
                     resp,
                 ]),
             })
def login(body: UserAuthorizationForm,
          db: Session = Depends(get_db)) -> TokenModel:
    try:

        user = UserCRUD.login(db, body)
        if not user.email_confirmed:
            raise UserNotActiveException.get()
        token = UserCRUD.generate_token(user)
        return resp.response(TokenModel(access_token=token))
    except AuthorizationException as e:
        raise e.get()
