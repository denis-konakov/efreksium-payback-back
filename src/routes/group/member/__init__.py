from fastapi import APIRouter

router = APIRouter(prefix='/member', tags=['member'])

from . import add


