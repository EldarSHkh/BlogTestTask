from pydantic import BaseModel, constr
from datetime import datetime


class RegisterForm(BaseModel):
    login: constr(strip_whitespace=True, min_length=1, max_length=50)
    password: constr(strip_whitespace=True, min_length=1, max_length=100)


class UserDTO(BaseModel):
    id: int
    login: constr(strip_whitespace=True, min_length=1, max_length=50)
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    user_id: int
    login: str
    exp: datetime
