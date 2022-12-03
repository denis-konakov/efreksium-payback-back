import sqlalchemy as q
from ..db_models import UserDatabaseModel
from .jwt import JWT
from sqlalchemy.orm import Session
from .models import *
from passlib.context import CryptContext
from .exc import *
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from config import Config
from time import time
import jwt

class UserCRUD:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def register(cls,
                 db: Session,
                 data: UserRegistrationData,
                 is_active: bool) -> UserPrivate:
        user = UserDatabaseModel(
            username=data.username,
            email=data.email,
            number=data.number,
            hashed_password=cls.pwd_context.hash(data.password),
            is_active=is_active
        )
        try:
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise UserAlreadyExistsException()
        db.refresh(user)
        return UserPrivate.from_orm(user)
    @classmethod
    def login(cls,
              db: Session,
              data: UserAuthorizationData) -> UserPrivate:
        user = db.query(UserDatabaseModel).filter_by(email=data.email).first()
        if user is None:
            raise UserNotFoundException()
        if not cls.pwd_context.verify(data.password, user.hashed_password):
            raise WrongPasswordException()
        return UserPrivate.from_orm(user)
    @classmethod
    def generate_token(cls,
                       user_id: int,
                       expires_delta: int | timedelta = Config.Settings.TOKEN_EXPIRE_INTERVAL) -> str:
        if isinstance(expires_delta, timedelta):
            expires_delta = expires_delta.total_seconds()
        expires_delta = int(time() + expires_delta)
        return JWT.encode({
            'id': user_id,
            'exp': expires_delta
        })

    @classmethod
    def get_user_by_token(cls,
                          db: Session,
                          token: str) -> UserPrivate:
        try:
            payload = JWT.decode(token)
        except jwt.exceptions.DecodeError:
            raise TokenDecodeException()
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredException()
        user = db.query(UserDatabaseModel).filter_by(id=payload['id']).first()
        if not user:
            raise UserNotFoundException()
        return UserPrivate.from_orm(user)
