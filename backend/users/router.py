import logging
from backend.config import SERVICE_NAME
from fastapi import APIRouter, Depends
from backend.auth.dependencies import get_current_user
from backend.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.users.schemas import UserOutSchema

router = APIRouter()

logger = logging.getLogger(f"{SERVICE_NAME}_logger")

@router.get("/me", summary="Get current user", response_model=UserOutSchema)
async def get_current_user_api(user: UserOutSchema = Depends(get_current_user)):
    return user