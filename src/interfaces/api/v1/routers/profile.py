from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException

from src.profile.application.dtos import (
    GetUserInfoRequestDTO,
    SearchUserInfoByNickNameRequestDTO,
    UpdateUserInfoRequestDTO,
    UserInfoListResponseDTO,
    UserInfoResponseDTO,
)
from src.profile.application.use_cases import (
    GetUserInfoUseCase,
    SearchUserInfoByNickNameUseCase,
    UpdateUserInfoUseCase,
)

from ..depends import get_user_id

profile_router = APIRouter()


@profile_router.get("/", response_model=UserInfoListResponseDTO)
@inject
async def search_users(
    nick_name: str,
    use_case: FromDishka[SearchUserInfoByNickNameUseCase],
    offset: int = 0,
    limit: int = 50,
    _: UUID = Depends(get_user_id),
):
    req = SearchUserInfoByNickNameRequestDTO(
        nick_name=nick_name, offset=offset, limit=limit
    )
    return await use_case.execute(req)


@profile_router.get("/{user_id}", response_model=UserInfoResponseDTO)
@inject
async def get_user_info(
    user_id: UUID,
    use_case: FromDishka[GetUserInfoUseCase],
    _: UUID = Depends(get_user_id),
):
    req = GetUserInfoRequestDTO(user_id=user_id)
    return await use_case.execute(req)


@profile_router.get("/me", response_model=UserInfoResponseDTO)
@inject
async def get_my_profile(
    use_case: FromDishka[GetUserInfoUseCase],
    user_id: UUID = Depends(get_user_id),
):
    req = GetUserInfoRequestDTO(user_id=user_id)
    return await use_case.execute(req)


@profile_router.put("/me", response_model=UserInfoResponseDTO)
@inject
async def update_my_profile(
    data: UpdateUserInfoRequestDTO,
    use_case: FromDishka[UpdateUserInfoUseCase],
    user_id: UUID = Depends(get_user_id),
):
    req = UpdateUserInfoRequestDTO(**data.model_dump(), user_id=user_id)
    return await use_case.execute(req)


@profile_router.put("/me/password")
@inject
async def change_my_profile_password(
    _: UUID = Depends(get_user_id),
):
    raise HTTPException(status_code=501, detail="Not implemented")


@profile_router.put("/me/email")
@inject
async def change_my_profile_email(
    _: UUID = Depends(get_user_id),
):
    raise HTTPException(status_code=501, detail="Not implemented")
