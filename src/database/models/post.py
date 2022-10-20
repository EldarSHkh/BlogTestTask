from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import DatetimeMixin


class Post(Base, DatetimeMixin):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(300), index=True)
    text = Column(String(10000))
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
