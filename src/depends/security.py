from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .db_connection import get_db, Session
from crud import UserCRUD, UserDatabaseModel
from utils.throws import throws
from crud.exceptions import InvalidTokenException
from config import Config

oauth2scheme = OAuth2PasswordBearer(
    tokenUrl=f"{Config.Settings.ROOT_PATH}/raw/token".replace('//', '/'),
    auto_error=False,
)

@throws([
    get_db,
    UserCRUD.get_user_by_token,
    InvalidTokenException
])
def get_current_user(token: str = Depends(oauth2scheme),
                     db: Session = Depends(get_db)) -> UserDatabaseModel:
    if token is None:
        raise InvalidTokenException()
    user = UserCRUD.get_user_by_token(db, token)
    return user




