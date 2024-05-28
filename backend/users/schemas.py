from datetime import datetime
from enum import Enum
from pydantic import BaseModel, validator


class UserOutSchema(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    last_login: datetime

    class Config:
        orm_mode = True