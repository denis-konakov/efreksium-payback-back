import time
import sqlalchemy as q
from config import Config
from loguru import logger
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
db_uri = f"postgresql://{Config.DB.USER}:{Config.DB.PASSWORD}@{Config.DB.HOST}:{Config.DB.PORT}/{Config.DB.DATABASE}"

while True:
    try:
        engine = q.create_engine(db_uri)
        engine.connect()
        break
    except Exception as e:  # noqa
        logger.error('Database is not ready yet, retrying in 5 seconds ({})', e)
        time.sleep(5)
logger.info('Database is ready')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(bind=engine)

__all__ = (
    'SessionLocal',
    'Base',
    'engine'
)

