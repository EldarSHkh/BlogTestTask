from fastapi import FastAPI
from src.api import configure_routers
from src.config import DbSettings
from src.database.models.base import DatabaseComponents


def build_app() -> FastAPI:
    app = FastAPI()
    db_settings = DbSettings()
    db_components = DatabaseComponents(db_settings.pg_dsn)
    app.include_router(configure_routers())
    app.state.db_components = db_components
    return app
