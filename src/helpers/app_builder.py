from fastapi import FastAPI
from fastapi.security import HTTPBearer
from argon2 import PasswordHasher

from src.api import configure_routers
from src.config import Settings
from src.database.models.base import DatabaseComponents
from src.database.repositories.user_repository import UserRepository
from src.database.repositories.post_repository import PostRepository
from src.database.repositories.comment_repository import CommentRepository
from src.api.dependencies.service import (
    UserServiceStub,
    JWTSecurityServiceStub,
    JWTSecurityGuardServiceStub,
    PostServiceStub,
    CommentServiceStub,
)
from src.services.user_service import UserService
from src.services.post_service import PostService
from src.services.comment_service import CommentService

from src.services.jwt_service import JWTAuthenticationService, JWTSecurityGuardService


def build_app() -> FastAPI:
    app = FastAPI()
    settings = Settings()
    db_components = DatabaseComponents(settings.pg_dsn)
    password_hasher = PasswordHasher()
    app.include_router(configure_routers())
    app.state.db_components = db_components
    app.dependency_overrides.update(
        {
            UserServiceStub: lambda: UserService(
                user_repository=UserRepository(
                    db_components.sessionmaker, password_hasher
                ),
            ),
            JWTSecurityServiceStub: lambda: JWTAuthenticationService(
                user_repository=UserRepository(
                    db_components.sessionmaker, password_hasher
                ),
                password_hasher=password_hasher,
                secret_key=settings.jwt_secret_key,
                algorithm="HS256",
                token_expires_in_minutes=settings.token_expires_in_minutes,
            ),
            JWTSecurityGuardServiceStub: JWTSecurityGuardService(
                auth_scheme=HTTPBearer(),
                user_repository=UserRepository(
                    db_components.sessionmaker, password_hasher
                ),
                password_hasher=password_hasher,
                secret_key=settings.jwt_secret_key,
                algorithm="HS256",
            ),
            PostServiceStub: lambda: PostService(
                post_repository=PostRepository(db_components.sessionmaker),
            ),
            CommentServiceStub: lambda: CommentService(
                comment_repository=CommentRepository(db_components.sessionmaker),
            ),
        }
    )
    return app
