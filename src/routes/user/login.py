from . import router
from depends import get_db, Depends, Session
from crud import UserAuthorizationData, UserPublic, UserCRUD, AuthorizationException
from fastapi import Response, HTTPException
from ..response import HTTPResponseModel, TokenModel
from fastapi.security import OAuth2PasswordRequestForm
@router.post(
    '/login',
    response_model=UserPublic,
    summary='Авторизация пользователя в системе',
    responses={
        200: {'description': 'Авторизация прошла успешно', 'model': TokenModel},
        401: {'description': 'Неверный логин или пароль', 'model': HTTPResponseModel},
        403: {'description': 'Пользователь не подтвердил почту', 'model': HTTPResponseModel},
    }
)
def login(form: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)) -> TokenModel:
    try:
        user = UserCRUD.login(db, UserAuthorizationData(username=form.username, password=form.password))
        if not user.is_active:
            raise HTTPException(status_code=403, detail='User is not active')
        token = UserCRUD.generate_token(user.id)
        return TokenModel(token=token)
    except AuthorizationException:
        raise HTTPException(
            status_code=401, detail="Incorrect username or password"
        )


