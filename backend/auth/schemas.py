from datetime import datetime
import logging
from pydantic import BaseModel, validator
from enum import Enum
from backend.config import SERVICE_NAME

from backend.users.queries import get_user_by_email_query

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


class RegisterOutSchema(BaseModel):
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

class RegisterInSchema(BaseModel):
    email: str
    first_name: str = ""
    last_name: str = ""
    password: str
    password2: str

    async def unique_email_validator(self, session):
        result = await get_user_by_email_query(self.email, session)
        if result:
            return False
        return True

    @validator('email')
    def email_is_valid(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email address')
        return v

    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if values['password'] != v:
            raise ValueError('Passwords do not match')
        return v

class LoginInSchema(BaseModel):
    email: str
    password: str

class LoginOutSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    class Config:
        orm_mode = True

class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
    jti: str = None

class RefreshTokenInSchema(BaseModel):
    refresh_token: str

class RefreshTokenOutSchema(BaseModel):
    access_token: str

class LogoutInSchema(BaseModel):
    refresh_token: str