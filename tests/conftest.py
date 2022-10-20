from typing import Any, AsyncGenerator

import pytest
from alembic import config as alembic_config, command
from fastapi import FastAPI
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def path_to_alembic_ini() -> str:
    from src.config import BASE_DIR
    return str(BASE_DIR / "alembic.ini")


@pytest.fixture(scope="session")
def path_to_migrations_folder() -> str:
    from src.config import BASE_DIR
    return str(BASE_DIR / "src" / "database" / "migrations")


@pytest.fixture(scope="session")
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



