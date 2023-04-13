from fastapi import APIRouter

router = APIRouter()

from .user import router as user_router
from .friends import router as friends_router
from .raw import router as raw_router
from .group import router as group_router

router.include_router(user_router)
router.include_router(friends_router)
router.include_router(raw_router)
router.include_router(group_router)
