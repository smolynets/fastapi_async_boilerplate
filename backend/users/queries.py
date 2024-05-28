
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.config import SERVICE_NAME
from backend.users.models import User
from datetime import datetime as dt
from uuid import uuid4

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


async def get_user_by_id_query(id: int, session: AsyncSession) -> User:
    result = await session.execute(select(User).filter(User.id == id))
    result = result.scalars().first()
    return result


async def get_user_by_email_query(email: str, session: AsyncSession) -> User:
    result = await session.execute(select(User).filter(User.email == email))
    result = result.scalars().first()
    return result

async def create_user_query(data: dict, session: AsyncSession) -> User:
    try:
        user = User(**data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    except Exception as e:
        logger.error(e)
        return None

async def update_user_query(id: int, data: dict, session: AsyncSession) -> User:
    try:
        query = update(User).where(User.id == id).values(**data).returning(User)
        result = await session.execute(query)
        await session.commit()
        return result.scalars().first()
    except Exception as e:
        logger.error(e)
        await session.rollback()
        return None
