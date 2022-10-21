from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref

from .base import Base
from .mixin import DatetimeMixin


class Comment(Base, DatetimeMixin):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    text = Column(String(500))
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    post = relationship("Post", back_populates="comments")
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    author = relationship("User", back_populates="comments")
    parent_id = Column(Integer, ForeignKey('comment.id', ondelete="SET NULL"), nullable=True)
    replies = relationship(
        "Comment",
        lazy="selectin", join_depth=10
    )

