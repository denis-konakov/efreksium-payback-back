import fastapi
from db import SessionLocal
from loguru import logger
from config import Config

from db import Base
import crud.db_models
Base.metadata.create_all()

app = fastapi.FastAPI()

from routes import router

app.include_router(router)


