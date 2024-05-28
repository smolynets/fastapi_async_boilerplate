import logging
from backend.config import SERVICE_NAME
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.auth.dependencies import get_current_user
from backend.auth.queries import add_expired_token_query, get_expired_token_query
from backend.auth.utils import create_access_token, create_refresh_token, decode_refresh_token, get_hashed_password, verify_password
from backend.database import get_db_session
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth.schemas import (LoginOutSchema, LogoutInSchema, RefreshTokenInSchema,
                                  RefreshTokenOutSchema,
                                   RegisterInSchema, RegisterOutSchema, LoginInSchema)
from backend.users.schemas import UserOutSchema
from backend.users.queries import create_user_query, get_user_by_email_query
from uuid import uuid4

router = APIRouter()

logger = logging.getLogger(f"{SERVICE_NAME}_logger")


@router.post("/token", summary="Login", response_model=LoginOutSchema)
async def login_api(data: LoginInSchema,  session: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_email_query(data.email, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not active")
    hashed_password = user.password_hash
    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = str(uuid4())
    return {"access_token": create_access_token(user.email, token), "refresh_token": create_refresh_token(user.email, token)}


@router.post("/logout", summary="Logout")
async def logout_api(data: LogoutInSchema,  session: AsyncSession = Depends(get_db_session), 
                    user: UserOutSchema = Depends(get_current_user)):
    token_data = decode_refresh_token(data.refresh_token)
    try:
        await add_expired_token_query(token_data.jti, user.id, session)
        return {"message": "OK"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")


@router.post("/token/refresh", summary="Refresh token", response_model=RefreshTokenOutSchema)
async def refresh_token_api(data: RefreshTokenInSchema,  session: AsyncSession = Depends(get_db_session)):
    token_data = decode_refresh_token(data.refresh_token)
    # check if jti in expired_token
    if await get_expired_token_query(token_data.jti, session):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token revoked")
    return {"access_token": create_access_token(token_data.sub, token_data.jti)}


@router.post("/swagger/token", summary="Login for swagger UI", response_model=LoginOutSchema)
async def login_swagger_api(data: OAuth2PasswordRequestForm = Depends(),  session: AsyncSession = Depends(get_db_session)):
    user = await get_user_by_email_query(data.username, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    hashed_password = user.password_hash
    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    token = str(uuid4())
    return {"access_token": create_access_token(user.email, token), "refresh_token": create_refresh_token(user.email, token)}


@router.post("/registration", summary="Registration", response_model=RegisterOutSchema)
async def register_api(data: RegisterInSchema, session: AsyncSession = Depends(get_db_session)):
    unique_email_check = await data.unique_email_validator(session)
    if not unique_email_check:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Email already exists")
    user_data = {
        "email": data.email,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "is_active": True,
        "password_hash": get_hashed_password(data.password)
    }
    new_user = await create_user_query(user_data, session)
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong")
    return new_user
