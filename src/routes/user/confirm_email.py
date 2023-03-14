from fastapi import Path

from . import router
from crud.user.models import UserPublic
from crud import UserCRUD
from depends import Session, Depends, get_db
from utils.response import ResponseException
from utils import throws, HTTPResponseModel
from crud.types import EmailConfirmationCode

resp = HTTPResponseModel.success('Подтверждение прошло успешно', UserPublic)

@router.get('/confirm_email/{code}',
            summary='Подтверждение почты',
            responses={
                **throws.docs([
                    UserCRUD.confirm_email,
                    resp,
                ]),
            })
def confirm_email(
        code: EmailConfirmationCode = Path(title='Код подтверждения'),
        db: Session = Depends(get_db)) -> UserPublic:
    try:
        user = UserCRUD.get(db, email=code.email)
        UserCRUD.confirm_email(user, code)
    except ResponseException as e:
        raise e.get()
    return resp.response(UserPublic.from_orm(user))


