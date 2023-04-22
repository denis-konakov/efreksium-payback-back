from fastapi import APIRouter

router = APIRouter(prefix='/group', tags=['group'])

from . import create
from . import all
from . import change_balance
from . import get
from .history import router as history_router
router.include_router(history_router)
from .member import router as member_router
router.include_router(member_router)
from .avatar import router as avatar_router
router.include_router(avatar_router)




