from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import DatetimeMixin


class User(Base, DatetimeMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    login = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
