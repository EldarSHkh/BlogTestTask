from __future__ import annotations

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


class CommentDTO(BaseModel):
    id: int
    post_id: int
    author_id: int
    parent_id: int = None
    text: constr(strip_whitespace=True, min_length=5, max_length=500)
    replies: list[CommentDTO] | CommentDTO = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class PostDTO(BaseModel):
    id: int
    title: constr(strip_whitespace=True, min_length=5, max_length=300)
    text: constr(strip_whitespace=True, min_length=5, max_length=10000)
    author_id: int
    comments: list[CommentDTO] = None
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


class UpdatePostSchema(BaseModel):
    title: constr(strip_whitespace=True, min_length=5, max_length=300) = None
    text: constr(strip_whitespace=True, min_length=5, max_length=10000) = None


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenPayload(BaseModel):
    user_id: int
    login: str
    exp: datetime
