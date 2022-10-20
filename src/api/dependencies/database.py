from abc import ABC

from src.database.repositories.base import Model


class UserRepositoryStub(ABC):

    async def add_user(self, *, login: str, password: str) -> Model:
        ...

    async def delete_user(self, user_id: int) -> None:
        ...

    async def get_user_by_id(self, user_id: int) -> Model:
        ...

    async def get_all_users(self) -> list[Model]:
        ...

    async def update_password_hash(self, new_pwd_hash: str, user_id: int) -> None:
        ...

    async def get_user_by_login(self, login: str) -> Model:
        ...
