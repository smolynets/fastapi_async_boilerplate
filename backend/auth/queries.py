import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.auth.models import ExpiredToken
from backend.config import SERVICE_NAME

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


async def get_expired_token_query(jti: str, session: AsyncSession) -> ExpiredToken:
    result = await session.execute(select(ExpiredToken).filter(ExpiredToken.jti == jti))
    result = result.scalars().first()
    return result

async def add_expired_token_query(jti: str, user_id: int, session: AsyncSession) -> ExpiredToken:
    new_expired_token = ExpiredToken(jti=jti, user_id=user_id)
    session.add(new_expired_token)
    await session.commit()
    return new_expired_token