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

    async def add_post(self, *, author_id: int, title: str, text: str) -> Model:
        return await self._insert(author_id=author_id, title=title, text=text)

    async def delete_post(self, *, author_id: int,  post_id: int) -> list[Model]:
        try:
            return await self._delete((self.model.id == post_id) & (self.model.author_id == author_id))
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def update_post(self,  author_id: int,  post_id: int, update_data: dict) -> list[Model]:
        try:
            return await self._update((self.model.id == post_id) & (self.model.author_id == author_id), **update_data)
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def get_post_by_id(self, post_id: int) -> Model:
        return await self._select_one(self.model.id == post_id)



