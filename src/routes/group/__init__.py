from fastapi import APIRouter

router = APIRouter(prefix='group', tags=['group'])

from . import create

