from fastapi import APIRouter

router = APIRouter(prefix='/friends', tags=['friends'])

from . import add
from . import get
