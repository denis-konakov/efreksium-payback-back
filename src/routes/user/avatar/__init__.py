from fastapi import APIRouter

router = APIRouter(prefix='/avatar', tags=['avatar'])

from . import create
from . import delete
