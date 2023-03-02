from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .db_connection import get_db, Session
from crud import UserCRUD, UserPrivate, ResponseException
from utils.throws import throws
oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

@throws([UserCRUD.get_user_by_token])
def get_current_user(token: str = Depends(oauth2scheme),
                     db: Session = Depends(get_db)) -> UserPrivate:
    try:
        user = UserCRUD.get_user_by_token(db, token)
        return UserPrivate.from_orm(user)
    except ResponseException as e:
        raise e.get()



