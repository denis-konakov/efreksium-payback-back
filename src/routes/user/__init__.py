from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['user'])

from . import login
from . import profile
from . import register
