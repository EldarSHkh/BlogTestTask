from fastapi import APIRouter

from .endpoints import auth, user


def configure_routers() -> APIRouter:
    base_api_router = APIRouter(prefix="/api")
    base_api_router.include_router(auth.api_router, tags=["auth"], prefix="/auth")
    base_api_router.include_router(user.api_router, tags=["user"], prefix="/users")

    return base_api_router

