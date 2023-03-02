from . import router
from depends import get_db, Depends, Session
from crud import UserAuthorizationForm, UserCRUD, AuthorizationException, UserNotActiveException, WrongPasswordException
from utils.response import HTTPResponseModel, TokenModel
from fastapi.security import OAuth2PasswordRequestForm
from utils.throws import throws
@router.post(
    '/login',
    summary='Авторизация пользователя в системе',
    responses={
        **throws.docs([
            UserCRUD.login,
            UserCRUD.generate_token
        ]),
        200: {
            'description': 'Авторизация прошла успешно',
            'model': TokenModel
        },
    }
)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)) -> TokenModel:
    try:
        user = UserCRUD.login(db, UserAuthorizationForm(email=form.username, password=form.password))
        if not user.is_active:
            raise UserNotActiveException.get()
        token = UserCRUD.generate_token(user.id)
        return TokenModel(access_token=token)
    except AuthorizationException as e:
        raise e.get()


