import jwt
from config import Config
class JWT:
    SESSION_KEY = Config.Secrets.SESSION_KEY
    ALGORITHM = 'HS256'
    @classmethod
    def encode(cls, payload: dict):
        return jwt.encode(payload, cls.SESSION_KEY, algorithm=cls.ALGORITHM)
    @classmethod
    def decode(cls, token: str):
        return jwt.decode(token, cls.SESSION_KEY, algorithms=[cls.ALGORITHM])
