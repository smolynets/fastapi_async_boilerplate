
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from backend.config import SERVICE_NAME
from backend.items.models import Item
from datetime import datetime as dt
from uuid import uuid4
from backend.items.schemas import ItemCreate, ItemUpdate

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


async def create_item(db: AsyncSession, item: ItemCreate):
    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Item).offset(skip).limit(limit))
    return result.scalars().all()

async def get_item(db: AsyncSession, item_id: int):
    result = await db.execute(select(Item).where(Item.id == item_id))
    return result.scalars().first()

async def update_item(db: AsyncSession, item_id: int, item: ItemUpdate):
    db_item = await get_item(db, item_id)
    if db_item:
        db_item.name = item.name
        db_item.description = item.description
        await db.commit()
        await db.refresh(db_item)
    return db_item

async def delete_item(db: AsyncSession, item_id: int):
    db_item = await get_item(db, item_id)
    if db_item:
        await db.delete(db_item)
        await db.commit()
    return db_item
