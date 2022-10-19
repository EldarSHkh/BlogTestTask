from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class DatetimeMixin:
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
