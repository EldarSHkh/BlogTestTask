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

from src.api.dependencies.service import CommentServiceStub, JWTSecurityGuardServiceStub
from src.api.dto import CommentDTO
from src.services.comment_service import CommentNotFound
from src.database.repositories.comment_repository import DbError

api_router = APIRouter(
    dependencies=[Depends(JWTSecurityGuardServiceStub), Depends(HTTPBearer())]
)


@api_router.get("/{comment_id}", response_model=CommentDTO)
async def get_comment(comment_id: int, comment_service: CommentServiceStub = Depends()):
    try:
        return await comment_service.get_comment(comment_id=comment_id)
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )


@api_router.post("", response_model=CommentDTO)
async def create_comment(
    request: Request,
    text: constr(strip_whitespace=True, min_length=5, max_length=500) = Body(),
    post_id: int = Body(),
    parent_id: None | int = Body(0),
    comment_service: CommentServiceStub = Depends(),
):
    """
    parent_id: id of the comment the user is replying to
    """
    try:
        return await comment_service.create_comment(
            author_id=request.state.user.user_id,
            text=text,
            post_id=post_id,
            parent_id=parent_id if parent_id != 0 else None,
        )
    except DbError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="error when creating a comment",
        )


@api_router.delete("/{comment_id}")
async def delete_comment(
    request: Request,
    comment_id: int = Path(...),
    comment_service: CommentServiceStub = Depends(),
):
    try:
        await comment_service.delete_comment(
            author_id=request.state.user.user_id, comment_id=comment_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )


@api_router.patch("/{comment_id}", response_model=CommentDTO)
async def update_comment(
    request: Request,
    comment_id: int,
    text: constr(strip_whitespace=True, min_length=5, max_length=500) = Body(
        embed=True
    ),
    post_service: CommentServiceStub = Depends(),
):
    try:
        return await post_service.update_comment(
            author_id=request.state.user.user_id,
            comment_id=comment_id,
            update_data={"text": text},
        )
    except CommentNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="comment not found"
        )
