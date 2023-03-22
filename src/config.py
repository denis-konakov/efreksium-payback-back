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
    class AttachmentsService:
        __prefix = 'ATTACHMENTS_SERVICE_'
        ENABLED:        bool = bool(os.getenv(f'{__prefix}ENABLED', False))
        PRIVATE_URL:    str = os.getenv(f'{__prefix}PRIVATE_URL', '')
        PUBLIC_URL:     str = os.getenv(f'{__prefix}PUBLIC_URL', '')
        SECRET_KEY:     str = os.getenv(f'{__prefix}SECRET_KEY', '')
    class Settings:
        TOKEN_EXPIRE_INTERVAL: int | timedelta = timedelta(days=7)
        ROOT_PATH:             str = os.getenv('ROOT_PATH', '/')
    class Email:
        __prefix = 'EMAIL_'
        ENABLED:            bool = bool(os.getenv(f'{__prefix}ENABLED', False))
        FROM:               str = os.getenv(f'{__prefix}FROM')
        FROM_NAME:          str = os.getenv(f'{__prefix}FROM_NAME')
        PASSWORD:           str = os.getenv(f'{__prefix}PASSWORD')
        SERVER:             str = os.getenv(f'{__prefix}SERVER')
        PORT:               int = int(os.getenv(f'{__prefix}PORT', 587))
        TLS:                bool = bool(os.getenv(f'{__prefix}TLS', False))
        SSL:                bool = bool(os.getenv(f'{__prefix}SSL', False))
        SSL_TLS:            bool = bool(os.getenv(f'{__prefix}SSL_TLS', False))
        USE_CREDENTIALS:    bool = bool(os.getenv(f'{__prefix}USE_CREDENTIALS', False))
        TEMPLATES_DIR:      str = os.getenv(f'{__prefix}TEMPLATES_DIR')

    class DB:
        __prefix = 'DATABASE_'
        URL: str = os.getenv(f'{__prefix}URL')
    class Secrets:
        SESSION_KEY = try_read('/deps/secrets/session_key.bin', 'rb', b'secret123').hex()
