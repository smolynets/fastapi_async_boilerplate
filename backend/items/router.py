import logging
from backend.config import SERVICE_NAME
from fastapi import APIRouter, Depends, HTTPException
from backend.auth.dependencies import get_current_user
from backend.database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.items.schemas import ItemCreate, ItemOutSchema, ItemUpdate
from backend.items.models import Item
from backend.items.queries import create_item, get_items, get_item, update_item, delete_item
from typing import List
from backend.users.schemas import UserOutSchema

router = APIRouter()

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


@router.post("/", summary="Items", response_model=ItemOutSchema)
async def create_item_api(
    item: ItemCreate,
    session: AsyncSession = Depends(get_db_session),
    user: UserOutSchema = Depends(get_current_user)
):
    return await create_item(session, item)


@router.get("/", response_model=List[ItemOutSchema])
async def get_item_api(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_db_session),
    user: UserOutSchema = Depends(get_current_user)
):
    return await get_items(session, skip, limit)


@router.get("/{item_id}", response_model=ItemOutSchema)
async def get_item_by_id_api(
    item_id: int,
    session: AsyncSession = Depends(get_db_session),
    user: UserOutSchema = Depends(get_current_user)
):
    db_item = await get_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/{item_id}", response_model=ItemOutSchema)
async def update_item_api(
    item_id: int, item: ItemUpdate,
    session: AsyncSession = Depends(get_db_session),
    user: UserOutSchema = Depends(get_current_user)
):
    db_item = await update_item(session, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete("/{item_id}", response_model=ItemOutSchema)
async def delete_item_api(
    item_id: int,
    session: AsyncSession = Depends(get_db_session),
    user: UserOutSchema = Depends(get_current_user)
):
    db_item = await delete_item(session, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
