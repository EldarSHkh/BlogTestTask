from fastapi import FastAPI
from argon2 import PasswordHasher

from src.api import configure_routers
from src.config import DbSettings
from src.database.models.base import DatabaseComponents
from src.database.repositories.user_repository import UserRepository
from src.api.dependencies.database import UserRepositoryStub


def build_app() -> FastAPI:
    app = FastAPI()
    db_settings = DbSettings()
    db_components = DatabaseComponents(db_settings.pg_dsn)
    password_hasher = PasswordHasher()
    app.include_router(configure_routers())
    app.state.db_components = db_components
    app.dependency_overrides.update(
        {
            UserRepositoryStub: lambda: UserRepository(
                db_components.sessionmaker, password_hasher
            ),
        }
    )
    return app
