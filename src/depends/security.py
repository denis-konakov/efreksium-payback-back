from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .db_connection import get_db, Session
from crud import UserCRUD, UserPrivate, TokenDecodeException, TokenExpiredException, UserNotFoundException
from routes.response import HTTPResponseModel

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def get_current_user(token: str = Depends(oauth2scheme),
                     db: Session = Depends(get_db)) -> UserPrivate:
    try:
        user = UserCRUD.get_user_by_token(db, token)
        return UserPrivate.from_orm(user)
    except TokenDecodeException:
        raise HTTPException(status_code=401, detail='Invalid token')
    except TokenExpiredException:
        raise HTTPException(status_code=401, detail='Token expired')
    except UserNotFoundException:
        raise HTTPException(status_code=401, detail='User not found')


get_current_user.responses = {
    401: {
        'description': 'Invalid token',
        'model': HTTPResponseModel
    }
}
