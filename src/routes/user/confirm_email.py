from fastapi import Path

from . import router
from crud.user.models import UserPublic
from crud import UserCRUD, cv
from depends import Session, Depends, get_db
from utils.response import ResponseException
from utils.throws import throws

@router.post(
    '/confirm_email/{code}',
    summary='Подтверждение почты',
    responses={
        **throws.docs([
            UserCRUD.confirm_user
        ]),
        200: {
            'description': 'Подтверждение прошло успешно',
            'model': UserPublic
        }
    }
)
def confirm_email(
        code: str = Path(title='Код подтверждения'),
        db: Session = Depends(get_db)) -> UserPublic:
    try:
        user = UserCRUD.confirm_user(db, code, cv.REGISTRATION)
        UserCRUD.set_user_active(db, user, True)
    except ResponseException as e:
        raise e.get()

    return UserPublic.from_orm(user)


