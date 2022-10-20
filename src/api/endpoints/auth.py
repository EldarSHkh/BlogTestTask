from fastapi import Depends, APIRouter, HTTPException, status, Response

from src.api.dependencies.service import UserServiceStub, JWTSecurityServiceStub
from src.api.dto import RegisterForm
from src.database.exceptions import DbError
from src.api.dto import AccessToken

api_router = APIRouter()


@api_router.post("/register")
async def user_registration(user: RegisterForm, user_service: UserServiceStub = Depends()):
    try:
        await user_service.user_registration(login=user.login, password=user.password)
        return Response(status_code=status.HTTP_201_CREATED)
    except DbError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user registration error")


@api_router.post("/login", response_model=AccessToken)
async def login(user: RegisterForm, jwt_service: JWTSecurityServiceStub = Depends()):
    token = await jwt_service.authenticate_user(user)
    return AccessToken(access_token=token)



