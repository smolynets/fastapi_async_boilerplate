
import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend import config
from sys import modules


# ==================== POSTGRES ====================

DATABASE_URL = f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.DATABASE}"


engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_models())

# ==================== REDIS ====================

# async def get_redis_client() -> Redis:
#     redis_client = Redis(host=config.REDIS_HOST, 
#                          port=config.REDIS_PORT, 
#                          db=0)
#     return redis_client