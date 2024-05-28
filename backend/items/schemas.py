from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator


class ItemCreate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True


class ItemOutSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime


class ItemUpdate(BaseModel):
    name: str
    description: str

    class Config:
        orm_mode = True