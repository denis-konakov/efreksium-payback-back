import os
from typing import overload
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
    class Email:
        ENABLED:            bool = bool(os.getenv('EMAIL_ENABLED', False))
        FROM:               str = os.getenv('EMAIL_FROM')
        FROM_NAME:          str = os.getenv('EMAIL_FROM_NAME')
        PASSWORD:           str = os.getenv('EMAIL_PASSWORD')
        SERVER:             str = os.getenv('EMAIL_SERVER')
        PORT:               int = int(os.getenv('EMAIL_PORT', 587))
        TLS:                bool = bool(os.getenv('EMAIL_TLS', False))
        SSL:                bool = bool(os.getenv('EMAIL_SSL', False))
        SSL_TLS:            bool = bool(os.getenv('EMAIL_SSL_TLS', False))
        USE_CREDENTIALS:    bool = bool(os.getenv('EMAIL_USE_CREDENTIALS', False))
        TEMPLATES_DIR:      str = os.getenv('EMAIL_TEMPLATES_DIR')

    class DB:
        HOST:       str = os.getenv('POSTGRES_HOST', 'localhost')
        PORT:       int = int(os.getenv('POSTGRES_PORT', '5432'))
        USER:       str = os.getenv('POSTGRES_USER', 'postgres')
        PASSWORD:   str = os.getenv('POSTGRES_PASSWORD', 'postgres')
        DATABASE:   str = os.getenv('POSTGRES_DB', 'postgres')
    class Secrets:
        SESSION_KEY = try_read('/secrets/session_key.bin', 'rb', b'secret123').hex()
