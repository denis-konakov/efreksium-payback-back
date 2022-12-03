from fastapi import APIRouter

router = APIRouter(prefix='/api')

from .user import router as user_router

router.include_router(user_router)