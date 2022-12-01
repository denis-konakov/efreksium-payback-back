import fastapi
from db import SessionLocal
from loguru import logger
from config import Config

import init_logger

app = fastapi.FastAPI()


