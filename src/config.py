import os
from datetime import timedelta

from loguru import logger
from typing import TypeVar
T = TypeVar('T')
def try_read(path: str, mode: str, default: T) -> T:
    try:
        with open(path, mode) as file:
            return file.read()
    except FileNotFoundError:
        logger.error('File not found: {}', path)
        return default
class Config:
    class Settings:
        TOKEN_EXPIRE_INTERVAL: int | timedelta = timedelta(days=7)
    class DB:
        HOST = os.getenv('POSTGRES_HOST', 'localhost')
        PORT = os.getenv('POSTGRES_PORT', '5432')
        USER = os.getenv('POSTGRES_USER', 'postgres')
        PASSWORD = os.getenv('POSTGRES_PASSWORD', 'postgres')
        DATABASE = os.getenv('POSTGRES_DB', 'postgres')
    class Secrets:
        SESSION_KEY = try_read('/secrets/session_key.bin', 'rb', b'secret123').hex()
