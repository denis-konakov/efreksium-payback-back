from fastapi import APIRouter

router = APIRouter()

from .user import router as user_router
from .friends import router as friends_router

router.include_router(user_router)
router.include_router(friends_router)

