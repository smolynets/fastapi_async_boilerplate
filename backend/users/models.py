from backend.database import Base
from datetime import datetime as dt

from sqlalchemy import (Boolean, Column, ForeignKey,
                        Integer, DateTime, String, JSON)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String, nullable=True, default=None)
    last_name = Column(String, nullable=True, default=None)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, index=True, default=dt.utcnow)
    last_login = Column(DateTime, index=True, default=dt.utcnow)

