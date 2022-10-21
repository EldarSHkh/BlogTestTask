from fastapi import Depends, APIRouter, HTTPException, status, Response, Path, Request, Body
from fastapi.security import HTTPBearer

from src.api.dependencies.service import UserServiceStub, JWTSecurityGuardServiceStub
from src.helpers import http_execptions_string
from src.helpers.permissions import check_is_owner
from src.services.user_service import UserNotFound

api_router = APIRouter(dependencies=[Depends(JWTSecurityGuardServiceStub), Depends(HTTPBearer())])


@api_router.get("/{user_id}")
async def get_user(user_id: int, user_service: UserServiceStub = Depends()):
    if user := await user_service.get_user_info(user_id=user_id):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=http_execptions_string.USER_DOES_NOT_EXIST_ERROR
    )


@api_router.delete("/{user_id}")
async def delete_user(
        request: Request,
        user_id: int = Path(...),
        user_service: UserServiceStub = Depends(),
):
    check_is_owner(user_id, request)
    try:
        await user_service.delete_user(user_id=user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=http_execptions_string.USER_DOES_NOT_EXIST_ERROR
        )


@api_router.put("/password")
async def update_password(
        request: Request,
        new_password: str = Body(),
        current_password: str = Body(),
        user_service: UserServiceStub = Depends(),
):
    await user_service.update_password(
        user_id=request.state.user.user_id,
        current_password=current_password,
        new_password=new_password
    )
    return {"message": "password changed successfully"}
