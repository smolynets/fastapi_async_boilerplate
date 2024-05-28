from fastapi import HTTPException, status
from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from pydantic import ValidationError

from backend.auth.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM, \
                                JWT_REFRESH_TOKEN_LIFETIME_MINUTES, JWT_REFRESH_SECRET_KEY
from backend.auth.schemas import TokenPayload

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], jti: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject), "jti": jti}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: Union[str, Any], jti: str, expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=JWT_REFRESH_TOKEN_LIFETIME_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject), "jti": jti}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM)
    return encoded_jwt

def decode_refresh_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, JWT_REFRESH_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data