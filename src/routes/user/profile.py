from fastapi import Depends
from depends import get_current_user
from crud import UserPublic, UserPrivate
from . import router
from utils.throws import throws
@router.get(
    '/profile',
    summary="Получение данных о пользователе",
    responses={
        **throws.docs([
            get_current_user
        ]),
        200: {
            'description': 'Получение данных пользователя',
            'model': UserPublic
        },
    }
)
def profile(user: UserPrivate = Depends(get_current_user)) -> UserPublic:
    return UserPublic.from_orm(user)
