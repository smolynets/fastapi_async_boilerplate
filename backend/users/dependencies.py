import logging
from typing import Union, Any
from datetime import datetime
from backend.config import SERVICE_NAME
from fastapi import Depends, HTTPException, status, Header
from backend.auth.schemas import TokenPayload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db_session

from backend.users.schemas import UserOutSchema
from backend.users.queries import get_user_by_id_query

logger = logging.getLogger(f"{SERVICE_NAME}_logger")

