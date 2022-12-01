import jwt
from config import Config
class JWT:
    SESSION_KEY = Config.Secrets.SESSION_KEY
    ALGORITHM = 'hs256'
    @classmethod
    def encode(cls, payload: dict):
        return jwt.encode(payload, cls.SESSION_KEY, algorithm=cls.ALGORITHM)
    @classmethod
    def decode(cls, token: str):
        try:
            return jwt.decode(token, cls.SESSION_KEY, algorithms=[cls.ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise ValueError('Invalid token')
        except jwt.exceptions.ExpiredSignatureError:
            raise ValueError('Token expired')