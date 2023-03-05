import sqlalchemy as q
from ..db_models import UserDatabaseModel, ConfirmationVariant as cv
from .jwt import JWT
from sqlalchemy.orm import Session
from .models import *
from passlib.context import CryptContext
from ..exceptions import *
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from config import Config
from time import time
from ..err_proxy import CRUDBase
import jwt
from secrets import token_bytes
import base64
from binascii import Error as BinasciiError
from utils.throws import throws
class UserCRUD(CRUDBase):
    cv = cv
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    @classmethod
    @throws([UserNotFoundException])
    def _get_model(cls, db: Session, user: UserPrivate) -> UserDatabaseModel:
        r = db.query(UserDatabaseModel).filter(
            q.or_(
                UserDatabaseModel.email == user.email,
                UserDatabaseModel.username == user.username,
                UserDatabaseModel.number == user.number
            )
        ).first()
        if r is None:
            raise UserNotFoundException()
        return r
    @classmethod
    @throws([UserAlreadyExistsException])
    def register(cls,
                 db: Session,
                 data: UserRegistrationForm,
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
    @throws([UserNotFoundException, WrongPasswordException])
    def login(cls,
              db: Session,
              data: UserAuthorizationForm) -> UserPrivate:
        user = db.query(UserDatabaseModel).filter_by(email=data.email).first()
        if user is None:
            raise UserNotFoundException()
        if not cls.pwd_context.verify(data.password, user.hashed_password):
            raise WrongPasswordException()
        return UserPrivate.from_orm(user)
    @classmethod
    @throws
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
    @throws([TokenDecodeException, TokenExpiredException, UserNotFoundException])
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
    @classmethod
    @throws([UserNotFoundException])
    def get_user_by_email(cls, db: Session, email: EmailStr) -> UserPrivate:
        user = db.query(UserDatabaseModel).filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        return UserPrivate.from_orm(user)
    @classmethod
    @throws([UserNotFoundException])
    def get_user_by_id(cls, db: Session, user_id: int) -> UserPrivate:
        user = db.query(UserDatabaseModel).filter_by(id=user_id).first()
        if user is None:
            raise UserNotFoundException()
        return UserPrivate.from_orm(user)
    @classmethod
    @throws([UserNotFoundException])
    def get_user_by_registration_data(cls, db: Session, data: UserRegistrationForm) -> UserPrivate:
        user = db.query(UserDatabaseModel).filter(
            q.or_(
                UserDatabaseModel.email == data.email,
                UserDatabaseModel.username == data.username,
                UserDatabaseModel.number == data.number
            )
        ).first()
        if user is None:
            raise UserNotFoundException()
        return UserPrivate.from_orm(user)
    @classmethod
    @throws([UserNotFoundException])
    def generate_confirmation_code(cls,
                                   db: Session,
                                   user: int | UserDatabaseModel,
                                   varint: cv) -> str:
        code = token_bytes(16).hex()
        scode = cls.pwd_context.hash(code)
        if not isinstance(user, UserDatabaseModel):
            user = db.query(UserDatabaseModel).filter_by(id=user).first()
        if user is None:
            raise UserNotFoundException()
        user.confirmation_code = scode
        user.confirmation_variant = varint
        db.commit()
        return base64.b64encode(
            f'{code}:{user.email}'.encode()
        ).decode()
    @classmethod
    @throws([WrongConfirmationCodeException, UserNotFoundException])
    def confirm_user(cls,
                     db: Session,
                     code: str,
                     variant: cv) -> UserPrivate:
        try:
            code, email = base64.b64decode(code).decode().split(':')
        except BinasciiError:
            raise WrongConfirmationCodeException()
        user = db.query(UserDatabaseModel).filter_by(email=email).first()
        if user is None:
            raise UserNotFoundException()
        if user.confirmation_variant != variant:
            raise WrongConfirmationCodeException()
        if not cls.pwd_context.verify(code, user.confirmation_code):
            raise WrongConfirmationCodeException()
        user.confirmation_code = None
        user.confirmation_variant = cv.NONE
        db.commit()
        return UserPrivate.from_orm(user)
    @classmethod
    @throws([UserNotFoundException])
    def set_user_active(cls, db: Session, user: UserPrivate, status: bool | None = None) -> UserPrivate:
        model = cls._get_model(db, user)
        if status is None:
            status = user.is_active
        if model.is_active != status:
            model.is_active = status
            db.commit()
            db.refresh(model)
        return UserPrivate.from_orm(model)

