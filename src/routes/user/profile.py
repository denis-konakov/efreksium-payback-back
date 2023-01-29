from fastapi import Depends
from depends import get_current_user
from crud import UserPublic, UserPrivate
from . import router

@router.get(
    '/profile',
    summary="Получение данных о пользователе",
    responses={
        **get_current_user.responses,
        200: {
            'description': 'Получение данных пользователя',
            'model': UserPublic
        }
    }
)
def profile(user: UserPrivate = Depends(get_current_user)) -> UserPublic:
    return UserPublic.from_orm(user)
