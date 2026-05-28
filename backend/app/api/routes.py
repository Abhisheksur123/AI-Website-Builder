from fastapi import APIRouter

from app.api.webchat import webchat_router

router = APIRouter()
router.include_router(webchat_router, prefix="/api")

