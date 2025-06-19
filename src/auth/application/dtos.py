from pydantic import BaseModel, EmailStr
from uuid import UUID


class LoginRequestDTO(BaseModel):
    email: EmailStr
    password: str


class RegisterRequestDTO(BaseModel):
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
