from abc import ABC

from src.api.dto import RegisterForm, PostDTO
from src.services.jwt_service import JWTToken


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


class PostServiceStub(ABC):

    async def create_post(self, *, author_id: int, title: str, text: str) -> PostDTO:
        ...

    async def get_post_by_id(self, *, post_id: int) -> PostDTO:
        ...

    async def delete_post(self, *, author_id, post_id: int) -> None:
        ...

    async def update_post(self, *, author_id: int, post_id: int, update_data: dict) -> PostDTO:
        ...
