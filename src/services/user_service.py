from argon2.exceptions import VerificationError

from fastapi import HTTPException, status

from src.helpers import http_execptions_string
from src.database.repositories.user_repository import UserRepository
from src.api.dto import UserDTO


class UserNotFound(Exception):
    pass


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def user_registration(self, *, login: str, password: str) -> None:
        await self.user_repository.add_user(login=login, password=password)

    async def delete_user(self, *, user_id: int) -> None:
        await self.user_repository.delete_user(user_id)

    async def get_user_info(self, *, user_id: int) -> UserDTO | None:
        if user := await self.user_repository.get_user_by_id(user_id=user_id):
            return UserDTO.from_orm(user)
        return None

    async def update_password(self, *, user_id: int, current_password: str, new_password: str) -> None:
        if not (user := await self.user_repository.get_user_by_id(user_id=user_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=http_execptions_string.USER_DOES_NOT_EXIST_ERROR,
            )
        try:
            self.user_repository.password_hasher.verify(user.password, current_password)
            await self.user_repository.update_password_hash(
                new_pwd_hash=self.user_repository.password_hasher.hash(new_password),
                user_id=user.id
            )
        except VerificationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.INCORRECT_LOGIN_INPUT,
            )