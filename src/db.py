import time
import sqlalchemy as q
from config import Config
from loguru import logger
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
db_uri = Config.DB.URL

while True:
    try:
        engine = q.create_engine(db_uri)
        engine.connect()
        break
    except Exception as e:  # noqa
        logger.error('Database is not ready yet, retrying in 5 seconds\n{}', e)
        time.sleep(5)
logger.info('Database is ready')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
T = declarative_base(bind=engine)

class Base(T):
    __abstract__ = True
    def session(self) -> Session:
        return SessionLocal.object_session(self)
    @classmethod
    def table(cls) -> str:
        return cls.__tablename__
__all__ = (
    'SessionLocal',
    'Base',
    'engine'
)

