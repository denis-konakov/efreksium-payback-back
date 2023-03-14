from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from .db_connection import get_db, Session
from crud import UserCRUD, UserDatabaseModel
from utils.throws import throws

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/raw/token")

@throws([
    get_db,
    UserCRUD.get_user_by_token,
])
def get_current_user(token: str = Depends(oauth2scheme),
                     db: Session = Depends(get_db)) -> UserDatabaseModel:
    user = UserCRUD.get_user_by_token(db, token)
    return user




