from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, RootModel


class LoginRequestDTO(BaseModel):
    email: EmailStr
    password: str


class RegisterRequestDTO(BaseModel):
    user_id: UUID
    email: EmailStr
    password: str


class AccessTokenRequestDTO(BaseModel):
    access_token: str


class RefreshTokenRequestDTO(BaseModel):
    refresh_token: str


class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    access_expires: int
    refresh_expires: int


class UserResponseDTO(BaseModel):
    user_id: UUID


class SessionsRequestDTO(BaseModel):
    user_id: UUID


class SessionDTO(BaseModel):
    session_id: UUID
    user_id: UUID
    created_at: datetime
    last_login: datetime | None = None


SessionsResponseDTO = RootModel[List[SessionDTO]]


class DeleteSessionRequestDTO(BaseModel):
    session_id: UUID
