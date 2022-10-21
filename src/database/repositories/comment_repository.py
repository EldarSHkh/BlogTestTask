import typing

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, selectinload, joinedload, subqueryload
from sqlalchemy import select
from sqlalchemy.sql import Executable

from src.database.exceptions import DbError
from src.database.models.comment import Comment
from src.database.repositories.base import BaseRepository, Model


class CommentRepository(BaseRepository):
    model = Comment

    def __init__(self, session_or_pool: typing.Union[sessionmaker, AsyncSession]):
        super().__init__(session_or_pool)

    async def add_comment(self, *, author_id: int, post_id: int, text: str, parent_id: int = None) -> Model:
        return await self._insert(author_id=author_id, post_id=post_id, text=text, parent_id=parent_id)

    async def delete_comment(self, *, author_id: int,  comment_id: int) -> list[Model]:
        try:
            return await self._delete((self.model.id == comment_id) & (self.model.author_id == author_id))
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def update_comment(self,  author_id: int,  comment_id: int, update_data: dict) -> list[Model]:
        try:
            return await self._update(
                (self.model.id == comment_id) & (self.model.author_id == author_id),
                **update_data
            )
        except IntegrityError as exc:
            raise DbError(exc=exc)

   # async def get_comment(self, comment_id: int) -> Model:
    #    return await self._select_one(self.model.id == comment_id)

    async def get_comment(self, comment_id: int) -> Model:
        stmt = select(self.model).where(self.model.id == comment_id).distinct(self.model.id)
        async with self.transaction():
            result = (
                (await self._session.execute(typing.cast(Executable, stmt)))
                    .scalars()
                    .first()
            )
        return typing.cast(Model, result)

