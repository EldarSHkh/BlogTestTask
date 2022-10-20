from datetime import datetime, timedelta
from typing import NewType, Any, Dict

import jwt
from argon2.exceptions import VerificationError
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from pydantic import ValidationError
from starlette import status
from starlette.requests import Request

from src.api.dto import RegisterForm, TokenPayload
from src.helpers import http_execptions_string
from src.database.repositories.user_repository import UserRepository
from src.helpers.password_hasher import PasswordHasherProto

JWTToken = NewType("JWTToken", str)


class UserIsUnauthorized(Exception):
    def __init__(self, hint: str):
        self.hint = hint


class JWTSecurityGuardService:

    def __init__(
            self,
            auth_scheme: HTTPBearer,
            user_repository: UserRepository,
            password_hasher: PasswordHasherProto,
            secret_key: str,
            algorithm: str,
    ):
        self._auth_scheme = auth_scheme
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def __call__(self, request: Request) -> TokenPayload:
        jwt_token = await self._auth_scheme(request)

        if jwt_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.TOKEN_IS_MISSING,
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_payload = self._decode_token(token=jwt_token.credentials)
        request.state.user = token_payload
        return token_payload

    def _decode_token(self, token: str) -> TokenPayload:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return TokenPayload(login=payload["login"], user_id=payload["user_id"], exp=payload["exp"])
        except (jwt.DecodeError, ValidationError) as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.TOKEN_IS_INCORRECT,
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.TOKEN_EXPIRED,
                headers={"WWW-Authenticate": "Bearer"},
            )


class JWTAuthenticationService:

    def __init__(
            self,
            user_repository: UserRepository,
            password_hasher: PasswordHasherProto,
            secret_key: str,
            algorithm: str,
            token_expires_in_minutes: float
    ):
        self._token_expires_in_minutes = token_expires_in_minutes
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    async def authenticate_user(self, form_data: RegisterForm) -> JWTToken:
        if not (user := await self._user_repository.get_user_by_login(form_data.login)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.INCORRECT_LOGIN_INPUT,
            )

        if self._password_hasher.check_needs_rehash(user.password):
            await self._user_repository.update_password_hash(
                new_pwd_hash=self._password_hasher.hash(form_data.password),
                user_id=user.id
            )
        try:
            self._password_hasher.verify(user.password, form_data.password)
        except VerificationError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=http_execptions_string.INCORRECT_LOGIN_INPUT,
            )
        return JWTToken(self._generate_jwt_token(
            {"sub": form_data.login, "login": form_data.login, "user_id": user.id})
        )

    def _generate_jwt_token(self, token_payload: Dict[str, Any]) -> str:
        token_payload = {
            "exp": datetime.utcnow() + timedelta(minutes=self._token_expires_in_minutes),
            **token_payload
        }
        filtered_payload = {k: v for k, v in token_payload.items() if v is not None}
        return jwt.encode(filtered_payload, self._secret_key, algorithm=self._algorithm)


