import typing

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.exceptions import DbError
from src.database.models.user import User
from src.database.repositories.base import BaseRepository, Model
from src.helpers.password_hasher import PasswordHasherProto


class UserRepository(BaseRepository):
    model = User

    def __init__(self, session_or_pool: typing.Union[sessionmaker, AsyncSession],
                 password_hasher: PasswordHasherProto):
        super().__init__(session_or_pool)
        self.password_hasher = password_hasher

    async def add_user(self, *, login: str, password: str) -> Model:
        prepared_payload = {"login": login, "password": self.password_hasher.hash(password)}
        try:
            return await self._insert(**prepared_payload)
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def delete_user(self, user_id: int) -> None:
        try:
            await self._delete(self.model.id == user_id)
        except IntegrityError as exc:
            raise DbError(exc=exc)

    async def get_user_by_login(self, login: str) -> Model:
        return await self._select_one(self.model.login == login)

    async def get_user_by_id(self, user_id: int) -> Model:
        return await self._select_one(self.model.id == user_id)

    async def get_all_users(self) -> typing.List[Model]:
        return await self._select_all()

    async def update_password_hash(self, new_pwd_hash: str, user_id: int) -> None:
        try:
            await self._update(self.model.id == user_id, password=new_pwd_hash)
        except IntegrityError as exc:
            raise DbError(exc=exc)
