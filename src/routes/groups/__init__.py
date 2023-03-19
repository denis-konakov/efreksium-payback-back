from fastapi import APIRouter

router = APIRouter(prefix='groups', tags=['groups'])

from . import create

