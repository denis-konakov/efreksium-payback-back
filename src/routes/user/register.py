from . import router
from fastapi import HTTPException
from crud import UserRegistrationData, UserCRUD, UserPublic, UserAlreadyExistsException
from depends import get_db, Session, Depends
from config import Config
from ..response import HTTPResponseModel
@router.post('/register',
             summary='Регистрация пользователя',
             responses={
                200: {'description': 'Регистрация прошла успешно', 'model': UserPublic},
                400: {'description': 'Пользователь с таким именем уже существует', 'model': HTTPResponseModel}
             })
def register(data: UserRegistrationData,
             db: Session = Depends(get_db)) -> UserPublic:
    try:
        user = UserCRUD.register(db, data, not Config.Email.ENABLED)
        if Config.Email.ENABLED:
            pass
        return UserPublic.from_orm(user)
    except UserAlreadyExistsException:
        user = UserCRUD.get
        raise HTTPException(status_code=400, detail='User already exists')
