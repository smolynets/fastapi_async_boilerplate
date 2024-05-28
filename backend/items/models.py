from backend.database import Base
from datetime import datetime as dt

from sqlalchemy import Column, Integer, DateTime, String


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    created_at = Column(DateTime, index=True, default=dt.utcnow)
