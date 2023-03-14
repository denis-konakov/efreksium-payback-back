from fastapi import APIRouter

router = APIRouter(prefix='/raw', tags=['Technical'], include_in_schema=False)

from . import token
