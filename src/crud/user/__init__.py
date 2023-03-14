import sqlalchemy as q
from ..db_models import UserDatabaseModel
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
from utils.throws import throws
from crud.types import *
from typing import overload
class UserCRUD(CRUDBase):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    @throws([
        UserAlreadyExistsException,
    ])
    def register(cls,
                 db: Session,
                 data: UserRegistrationForm,
                 email_confirmed: bool) -> UserDatabaseModel:
        user = UserDatabaseModel(
            username=data.username,
            email=data.email,
            number=data.number,
            hashed_password=cls.pwd_context.hash(data.password),
            email_confirmed=email_confirmed
        )
        try:
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise UserAlreadyExistsException()
        db.refresh(user)
        return user

    @classmethod
    @throws([
        UserNotFoundException,
        WrongPasswordException,
    ])
    def login(cls,
              db: Session,
              data: UserAuthorizationForm) -> UserDatabaseModel:
        user = db.query(UserDatabaseModel).filter_by(email=data.email).first()
        if user is None:
            raise UserNotFoundException()
        if not cls.pwd_context.verify(data.password, user.hashed_password):
            raise WrongPasswordException()
        return user

    @classmethod
    @throws([

    ])
    def generate_token(cls,
                       user: UserDatabaseModel,
                       expires_delta: int | timedelta = Config.Settings.TOKEN_EXPIRE_INTERVAL) -> str:
        if isinstance(expires_delta, timedelta):
            expires_delta = expires_delta.total_seconds()
        expires_delta = int(time() + expires_delta)
        return JWT.encode({
            'id': user.id,
            'exp': expires_delta
        })
    @classmethod
    @throws([

    ])
    def _generate_email_code(cls,
                             email: EmailStr) -> PublicPrivateCodePair:
        return EmailConfirmationCode.generate(cls.pwd_context, email)

    @classmethod
    @throws([
        UserAlreadyExistsException,
        _generate_email_code,
    ])
    def generate_email_confirmation_code(cls,
                                         user: UserDatabaseModel) -> PublicPrivateCodePair:
        code = cls._generate_email_code(EmailStr(user.email))
        if user.email_confirmed:
            raise UserAlreadyExistsException()
        user.email_confirmation_code = code.public
        db = user.session()
        db.commit()
        db.refresh(user)
        return code

    @classmethod
    @throws([
        _generate_email_code
    ])
    def generate_reset_password_code(cls,
                                     user: UserDatabaseModel) -> PublicPrivateCodePair:
        code = cls._generate_email_code(EmailStr(user.email))
        user.password_reset_code = code.public
        db = user.session()
        db.commit()
        db.refresh(user)
        return code

    @classmethod
    @throws([
        TokenDecodeException,
        TokenExpiredException,
        UserNotFoundException,
    ])
    def get_user_by_token(cls,
                          db: Session,
                          token: str) -> UserDatabaseModel:
        try:
            payload = JWT.decode(token)
        except jwt.exceptions.DecodeError:
            raise TokenDecodeException()
        except jwt.exceptions.ExpiredSignatureError:
            raise TokenExpiredException()
        user = db.query(UserDatabaseModel).filter_by(id=payload['id']).first()
        if not user:
            raise UserNotFoundException()
        return user

    @classmethod
    @throws([
        UserAlreadyExistsException,
        WrongConfirmationCodeException,

    ])
    def confirm_email(cls,
                      user: UserDatabaseModel,
                      code: EmailConfirmationCode) -> UserDatabaseModel:
        if user.email_confirmed:
            raise UserAlreadyExistsException()
        if user.email_confirmation_code is None or not code.verify(cls.pwd_context, user.email_confirmation_code):
            raise WrongConfirmationCodeException()
        db = user.session()
        user.email_confirmed = True
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    @throws([
        WrongConfirmationCodeException,
    ])
    def confirm_password_reset(cls,
                               user: UserDatabaseModel,
                               code: EmailConfirmationCode,
                               new_password: str) -> UserDatabaseModel:
        if user.password_reset_code is None or not code.verify(cls.pwd_context, user.password_reset_code):
            raise WrongConfirmationCodeException()
        db = user.session()
        user.email_confirmation_code = None
        user.hashed_password = cls.pwd_context.hash(new_password)
        db.commit()
        db.refresh(user)
        return user

    @classmethod
    @overload
    def get(cls, db: Session, *, id: int) -> UserDatabaseModel: ...
    @classmethod
    @overload
    def get(cls, db: Session, *, email: EmailStr) -> UserDatabaseModel: ...
    @classmethod
    @throws([
        UserNotFoundException,
    ])
    def get(cls,
            db: Session, *,
            id: int | None = None,
            email: EmailStr | None = None) -> UserDatabaseModel:
        try:
            if id is not None:
                user = db.query(UserDatabaseModel).filter_by(id=id).first()
            elif email is not None:
                user = db.query(UserDatabaseModel).filter_by(email=email).first()
            else:
                raise ValueError()
            assert user is not None
        except AssertionError:
            raise UserNotFoundException()
        return user


