from datetime import datetime, timezone
from uuid import uuid4

from dishka import FromDishka

from src.auth.application.dtos import RegisterRequestDTO
from src.auth.application.use_cases import RegisterUseCase
from src.profile.application.dtos import CreateUserInfoRequestDTO
from src.profile.application.use_cases import CreateUserInfoUseCase

from ..dtos.auth import (
    RegistrationCompositeRequestDTO,
    RegistrationCompositeResponseDTO,
)
from .base import BaseUseCase


class RegistrationCompositeUseCase(BaseUseCase):
    def __init__(
        self,
        registration_use_case: FromDishka[RegisterUseCase],
        create_user_use_case: FromDishka[CreateUserInfoUseCase],
    ):
        self.__registration_use_case = registration_use_case
        self.__create_user_use_case = create_user_use_case

    async def execute(
        self, request: RegistrationCompositeRequestDTO
    ) -> RegistrationCompositeResponseDTO:
        user_id = uuid4()
        tokens = await self.__registration_use_case.execute(
            RegisterRequestDTO(
                user_id=user_id, email=request.email, password=request.password
            )
        )
        await self.__create_user_use_case(
            CreateUserInfoRequestDTO(
                user_id=user_id,
                first_name=request.first_name,
                last_name=request.last_name,
                nick_name=request.nick_name,
                date_of_birth=request.date_of_birth,
                created_at=datetime.now(timezone.utc),
            )
        )
        return tokens
