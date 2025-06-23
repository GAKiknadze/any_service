from abc import ABC, abstractmethod
from ..domain import entities, repositories
from . import dtos


class UserUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass

class CreateUserInfoUseCase(UserUseCase):
    def __init__(
        self,
        user_info_repository: repositories.UserInfoRepository
    ):
        self.__user_info_repository = user_info_repository

    async def execute(self, request: dtos.CreateUserInfoRequestDTO) -> dtos.UserInfoResponseDTO:
        user_info = entities.UserInfo(
            user_id=request.user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            nick_name=request.nick_name,
            date_of_birth=request.date_of_birth,
            avatar=request.avatar,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )
        created = await self.__user_info_repository.create(user_info)
        return dtos.UserInfoResponseDTO.model_validate(created, from_attributes=True)

class GetUserInfoUseCase(UserUseCase):
    def __init__(
        self,
        user_info_repository: repositories.UserInfoRepository
    ):
        self.__user_info_repository = user_info_repository

    async def execute(self, request: dtos.GetUserInfoRequestDTO) -> dtos.UserInfoResponseDTO:
        user_info = await self.__user_info_repository.get(request.user_id)
        return dtos.UserInfoResponseDTO.model_validate(user_info, from_attributes=True)

class SearchUserInfoByNickNameUseCase(UserUseCase):
    def __init__(
        self,
        user_info_repository: repositories.UserInfoRepository
    ):
        self.__user_info_repository = user_info_repository

    async def execute(self, request: dtos.SearchUserInfoByNickNameRequestDTO) -> dtos.UserInfoListResponseDTO:
        users = await self.__user_info_repository.get_by_nick_name(
            request.nick_name, offset=request.offset, limit=request.limit
        )
        return dtos.UserInfoListResponseDTO.model_validate(users, from_attributes=True)

class UpdateUserInfoUseCase(UserUseCase):
    def __init__(
        self,
        user_info_repository: repositories.UserInfoRepository
    ):
        self.__user_info_repository = user_info_repository

    async def execute(self, request: dtos.UpdateUserInfoRequestDTO) -> dtos.UserInfoResponseDTO:
        user_info = entities.UserInfo(
            user_id=request.user_id,
            first_name=request.first_name,
            last_name=request.last_name,
            nick_name=request.nick_name,
            date_of_birth=request.date_of_birth,
            avatar=request.avatar,
            created_at=request.created_at,
            updated_at=request.updated_at,
        )
        updated = await self.__user_info_repository.update(user_info)
        return dtos.UserInfoResponseDTO.model_validate(updated, from_attributes=True)
