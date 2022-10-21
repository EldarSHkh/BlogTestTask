from __future__ import annotations

import contextlib
import typing
from abc import ABC

from sqlalchemy import lambda_stmt, select, update, exists, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import Executable


Model = typing.TypeVar("Model")


class BaseRepository(ABC):

    model: typing.ClassVar[typing.Type[Model]]

    def __init__(
        self, session_or_pool: typing.Union[sessionmaker, AsyncSession]
    ) -> None:
        """
        :param session_or_pool: async session from async context manager
        """
        if isinstance(session_or_pool, sessionmaker):
            self._session: AsyncSession = typing.cast(AsyncSession, session_or_pool())
        else:
            self._session = session_or_pool

    @contextlib.asynccontextmanager
    async def transaction(self) -> typing.AsyncGenerator:
        if not self._session.in_transaction() and self._session.is_active:
            async with self._session.begin() as transaction:
                yield transaction
        else:
            yield

    async def _insert(self, **values: typing.Any) -> Model:
        async with self.transaction():
            insert_stmt = insert(self.model).values(**values).returning(self.model)
            result = (await self._session.execute(insert_stmt)).mappings().first()
        return self._convert_to_model(typing.cast(typing.Dict[str, typing.Any], result))

    async def _select_all(self, *clauses: typing.Any) -> typing.List[Model]:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self.transaction():
            result = (
                (await self._session.execute(typing.cast(Executable, stmt)))
                .scalars()
                .all()
            )
        return result

    async def _select_one(self, *clauses: typing.Any) -> Model:
        query_model = self.model
        stmt = lambda_stmt(lambda: select(query_model))
        stmt += lambda s: s.where(*clauses)
        async with self.transaction():
            result = (
                (await self._session.execute(typing.cast(Executable, stmt)))
                .scalars()
                .first()
            )
        return typing.cast(Model, result)

    async def _update(self, *clauses: typing.Any, **values: typing.Any) -> list[Model]:
        async with self.transaction():
            stmt = update(self.model).where(*clauses).values(**values).returning("*")
            result = (await self._session.execute(stmt)).mappings().all()
        return list(map(self._convert_to_model, result))

    async def _exists(self, *clauses: typing.Any) -> bool | None:
        stmt = exists(select(self.model).where(*clauses)).select()
        result = (await self._session.execute(stmt)).scalar()
        return typing.cast(typing.Optional[bool], result)

    async def _delete(self, *clauses: typing.Any) -> list[Model]:
        async with self.transaction():
            stmt = delete(self.model).where(*clauses).returning("*")
            result = (await self._session.execute(stmt)).mappings().all()
        return list(map(self._convert_to_model, result))

    def _convert_to_model(self, kwargs) -> Model:
        return self.model(**kwargs)
