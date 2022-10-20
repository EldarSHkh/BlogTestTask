from fastapi import APIRouter

from .endpoints import auth, user, post


def configure_routers() -> APIRouter:
    base_api_router = APIRouter(prefix="/api")
    base_api_router.include_router(auth.api_router, tags=["auth"], prefix="/auth")
    base_api_router.include_router(user.api_router, tags=["users"], prefix="/users")
    base_api_router.include_router(post.api_router, tags=["posts"], prefix="/posts")
    return base_api_router

