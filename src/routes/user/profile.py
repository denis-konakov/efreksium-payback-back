from fastapi import Depends
from depends import get_current_user
from crud import UserPublic, UserPrivate
from . import router
from utils.throws import throws
from utils import HTTPResponseModel
resp = HTTPResponseModel.success(
    'Получение данных пользователя',
    UserPublic
)
@router.get(
    '/profile',
    summary="Получение данных о пользователе",
    responses={
        **throws.docs([
            get_current_user,
            resp
        ]),
    }
)
def profile(user: UserPrivate = Depends(get_current_user)) -> UserPublic:
    return resp.response(response=UserPublic.from_orm(user))
