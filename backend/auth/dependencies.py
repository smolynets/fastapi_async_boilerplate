import logging
from typing import Union, Any
from datetime import datetime
from backend.config import SERVICE_NAME
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from backend.auth.schemas import TokenPayload
from sqlalchemy.ext.asyncio import AsyncSession
from backend.auth.queries import get_expired_token_query
from backend.database import get_db_session

from backend.users.schemas import UserOutSchema
from backend.users.queries import get_user_by_email_query
from .utils import (
    JWT_ALGORITHM,
    JWT_SECRET_KEY
)

from jose import jwt
from pydantic import ValidationError

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/swagger/token",
    scheme_name="JWT"
)

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


async def get_current_user(token: str = Depends(reuseable_oauth), session: AsyncSession = Depends(get_db_session)) -> UserOutSchema:
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # check if jti in expired_token
        if await get_expired_token_query(token_data.jti, session):
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = await get_user_by_email_query(token_data.sub, session)
    
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is inactive",
        )
    user = user.__dict__
    return UserOutSchema(**user)