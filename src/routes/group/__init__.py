from fastapi import APIRouter

router = APIRouter(prefix='/group', tags=['group'])

from . import create
from . import all
from .history import router as history_router
router.include_router(history_router)




