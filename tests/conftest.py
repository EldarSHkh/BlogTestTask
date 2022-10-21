import asyncio
from datetime import datetime, timedelta

from typing import Any, AsyncGenerator

import pytest
import jwt
from argon2 import PasswordHasher
from alembic import config as alembic_config, command
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker

from src.database.repositories.user_repository import UserRepository
from src.database.repositories.post_repository import PostRepository
from src.config import Settings


@pytest.fixture(scope='session')
def event_loop():
    return asyncio.new_event_loop()


@pytest.fixture(scope="module")
def path_to_alembic_ini() -> str:
    from src.config import BASE_DIR
    return str(BASE_DIR / "alembic.ini")


@pytest.fixture(scope="module")
def path_to_migrations_folder() -> str:
    from src.config import BASE_DIR
    return str(BASE_DIR / "src" / "database" / "migrations")


@pytest.fixture(scope="module")
def apply_migrations(path_to_alembic_ini: str, path_to_migrations_folder: str) -> AsyncGenerator[None, Any]:
    alembic_cfg = alembic_config.Config(path_to_alembic_ini)
    alembic_cfg.set_main_option('script_location', path_to_migrations_folder)
    command.upgrade(alembic_cfg, 'head')
    yield
    command.downgrade(alembic_cfg, 'base')


@pytest.fixture(scope="module")
def app(apply_migrations: None) -> FastAPI:
    from src.helpers.app_builder import build_app
    return build_app()


@pytest.fixture(scope="module")
def session_maker(app: FastAPI) -> sessionmaker:
    return app.state.db_components.sessionmaker


@pytest.fixture(scope="module")
def user_repository(session_maker: sessionmaker) -> UserRepository:
    return UserRepository(session_maker, PasswordHasher())


@pytest.fixture(scope="module")
def post_repository(session_maker: sessionmaker) -> PostRepository:
    return PostRepository(session_maker)


@pytest.fixture(scope="module")
async def test_user(user_repository: UserRepository):
    await user_repository.add_user(login="string", password="string")


@pytest.fixture(scope="module")
def token(test_user: None) -> str:
    settings = Settings()
    token_payload = {
        "exp": datetime.utcnow() + timedelta(minutes=settings.token_expires_in_minutes),
        "sub": "string",
        "login": "string",
        "user_id": 1
    }
    filtered_payload = {k: v for k, v in token_payload.items() if v is not None}
    return jwt.encode(filtered_payload, settings.jwt_secret_key, algorithm="HS256")
