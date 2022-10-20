from abc import ABC

from src.api.dto import RegisterForm
from src.services.security.jwt_service import JWTToken


class UserServiceStub(ABC):

    async def user_registration(self, *, login: str, password: str):
        ...

    async def delete_user(self, user_id: int) -> None:
        ...

    async def get_user_info(self, user_id: int):
        ...

    async def update_password(self, *, user_id: int, current_password: str, new_password: str) -> None:
        ...


class JWTSecurityServiceStub(ABC):

    async def authenticate_user(self, form_data: RegisterForm) -> JWTToken:
        ...


class JWTSecurityGuardServiceStub(ABC):
    pass

