from fastapi import APIRouter

router = APIRouter(prefix='/history', tags=['history'])

from . import get

