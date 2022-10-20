import typing

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.exceptions import DbError
from src.database.models.post import Post
from src.database.repositories.base import BaseRepository, Model


class PostRepository(BaseRepository):
    model = Post

    def __init__(self, session_or_pool: typing.Union[sessionmaker, AsyncSession]):
        super().__init__(session_or_pool)

    async def add_post(self, *, title: str, text: str) -> Model:
        async with self.transaction():
            return await self._insert(title=title, text=text)

    async def delete_post(self, post_id: int) -> None:
        try:
            await self._delete(self.model.id == post_id)
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def update_post(self, post_id: int):
        try:
            await self._update(self.model.id == post_id)
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def get_post_by_id(self, post_id: int) -> Model:
        return await self._select_one(self.model.id == post_id)



