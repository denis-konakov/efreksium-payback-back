from fastapi import Depends
from depends import get_current_user
from crud import UserDatabaseModel, UserPublicWithGroups, GroupDatabaseModel
from . import router
from utils.throws import throws
from utils import HTTPResponseModel
resp = HTTPResponseModel.success(
    'Получение данных пользователя',
    UserPublicWithGroups
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
def profile(user: UserDatabaseModel = Depends(get_current_user)) -> UserPublicWithGroups:
    return resp.response(
        UserPublicWithGroups.from_orm(user)
    )
