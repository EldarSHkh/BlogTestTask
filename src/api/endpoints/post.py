from fastapi import (
    Depends,
    APIRouter,
    HTTPException,
    status,
    Response,
    Path,
    Request,
    Body,
)
from fastapi.security import HTTPBearer
from pydantic import constr

from src.api.dependencies.service import PostServiceStub, JWTSecurityGuardServiceStub
from src.api.dto import PostDTO, UpdatePostSchema
from src.services.post_service import PostNotFound

api_router = APIRouter(
    dependencies=[Depends(JWTSecurityGuardServiceStub), Depends(HTTPBearer())]
)


@api_router.get("/{post_id}", response_model=PostDTO)
async def get_post(post_id: int, post_service: PostServiceStub = Depends()):
    try:
        return await post_service.get_post_by_id(post_id=post_id)
    except PostNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )


@api_router.post("", response_model=PostDTO)
async def create_post(
    request: Request,
    title: constr(strip_whitespace=True, min_length=5, max_length=300) = Body(),
    text: constr(strip_whitespace=True, min_length=5, max_length=10000) = Body(),
    post_service: PostServiceStub = Depends(),
):
    return await post_service.create_post(
        author_id=request.state.user.user_id, title=title, text=text
    )


@api_router.delete("/{post_id}")
async def delete_post(
    request: Request,
    post_id: int = Path(...),
    post_service: PostServiceStub = Depends(),
):
    try:
        await post_service.delete_post(
            author_id=request.state.user.user_id, post_id=post_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PostNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )


@api_router.patch("/{post_id}")
async def update_post(
    request: Request,
    post_id: int,
    update_data: UpdatePostSchema,
    post_service: PostServiceStub = Depends(),
):
    try:
        return await post_service.update_post(
            author_id=request.state.user.user_id,
            post_id=post_id,
            update_data=update_data.dict(exclude_none=True),
        )
    except PostNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="post not found"
        )
