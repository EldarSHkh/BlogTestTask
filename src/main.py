from fastapi import FastAPI
from src.helpers.app_builder import build_app


def create_app() -> FastAPI:
    return build_app()
