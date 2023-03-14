from . import router
from depends import Depends, get_db, Session
from fastapi.security import OAuth2PasswordRequestForm
from crud import UserCRUD, UserAuthorizationForm
from crud.exceptions import *
from utils import TokenModel, throws, HTTPResponseModel

@router.post('/token',
             summary='Получение токена',
             responses={
                 **throws.docs([
                    get_db,
                     UserCRUD.login,
                     UserNotActiveException,
                     UserCRUD.generate_token,
                 ]),
                 200: {'model': TokenModel, 'description': 'Получение токена без обертки'}
             })
def get_raw_token(form: OAuth2PasswordRequestForm = Depends(),
                  db: Session = Depends(get_db)) -> TokenModel:
    try:
        user = UserCRUD.login(db, UserAuthorizationForm(email=form.username, password=form.password))
        if not user.email_confirmed:
            raise UserNotActiveException.get()
        token = UserCRUD.generate_token(user)
        return TokenModel(access_token=token)
    except AuthorizationException as e:
        raise e.get()
