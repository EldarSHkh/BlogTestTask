from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import DatetimeMixin


class User(Base, DatetimeMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    posts = relationship("Posts", back_populates="post_author")
    comments = relationship("Comments", back_populates="author")
