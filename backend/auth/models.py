from backend.database import Base
from datetime import datetime as dt

from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, DateTime, String, JSON)
from sqlalchemy.orm import relationship
from backend.users.models import User


class ExpiredToken(Base):
    __tablename__ = "expired_token"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    jti = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, index=True, default=dt.utcnow)

    