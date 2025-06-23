from datetime import date, datetime
from typing import List
from uuid import UUID
from pydantic import BaseModel, RootModel

class CreateUserInfoRequestDTO(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    nick_name: str
    date_of_birth: date
    avatar: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

class GetUserInfoRequestDTO(BaseModel):
    user_id: UUID

class SearchUserInfoByNickNameRequestDTO(BaseModel):
    nick_name: str
    offset: int = 0
    limit: int = 50

class UpdateUserInfoRequestDTO(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    nick_name: str
    date_of_birth: date
    avatar: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

class UserInfoResponseDTO(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    nick_name: str
    date_of_birth: date
    avatar: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

class UserInfoListResponseDTO(RootModel[List[UserInfoResponseDTO]]):
    pass
