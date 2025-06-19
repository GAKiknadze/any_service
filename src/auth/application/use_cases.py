from ..domain import repositories, services, exceptions, entities
from . import dtos
from abc import ABC, abstractmethod
from uuid import uuid4
from datetime import datetime, timezone


class AuthUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass


class LoginUseCase(AuthUseCase):
    def __init__(
        self,
        auth_user_repository: repositories.AuthUserRepository,
        auth_session_repository: repositories.AuthSessionRepository,
        password_service: services.PasswordService,
        token_service: services.TokenService,
    ):
        self.__auth_user_repository = auth_user_repository
        self.__auth_session_repository = auth_session_repository
        self.__password_service = password_service
        self.__token_service = token_service

    async def execute(self, request: dtos.LoginRequestDTO) -> dtos.TokenResponseDTO:
        user = await self.__auth_user_repository.get_by_email(request.email)

        if not await self.__password_service.verify_password(
            request.password, user.password_hash
        ):
            raise exceptions.InvalidCredentialsExc()

        session = await self.__auth_session_repository.create(
            entities.AuthSession(
                session_id=uuid4(),
                user_id=user.id,
                created_at=datetime.now(timezone.utc),
                last_login=datetime.now(timezone.utc),
            )
        )

        access_token, access_exp = self.__token_service.create_access_token(
            user.id, session.session_id
        )
        refresh_token, refresh_exp = self.__token_service.create_refresh_token(
            user.id, session.id
        )

        return dtos.TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            access_expires=access_exp,
            refresh_expires=refresh_exp,
        )


class RegisterUseCase(AuthUseCase):
    def __init__(
        self,
        auth_user_repository: repositories.AuthUserRepository,
        auth_session_repository: repositories.AuthSessionRepository,
        password_service: services.PasswordService,
        token_service: services.TokenService,
    ):
        self.__auth_user_repository = auth_user_repository
        self.__auth_session_repository = auth_session_repository
        self.__password_service = password_service
        self.__token_service = token_service

    async def execute(self, request: dtos.RegisterRequestDTO) -> dtos.TokenResponseDTO:
        try:
            if await self.__auth_user_repository.get_by_email(request.email):
                raise exceptions.ContactAlreadyExistsExc()
        except exceptions.UserNotFoundExc:
            ...

        password_hash = self.__password_service.hash_password(request.password)

        user = await self.__auth_user_repository.create(
            entities.AuthUser(
                id=uuid4(),
                email=request.email,
                password_hash=password_hash,
                created_at=datetime.now(timezone.utc),
                last_modified=datetime.now(timezone.utc),
            )
        )

        session = await self.__auth_session_repository.create(
            entities.AuthSession(
                session_id=uuid4(),
                user_id=user.id,
                created_at=datetime.now(timezone.utc),
                last_login=datetime.now(timezone.utc),
            )
        )

        access_token, access_exp = self.__token_service.create_access_token(
            user.id, session.session_id
        )
        refresh_token, refresh_exp = self.__token_service.create_refresh_token(
            user.id, session.session_id
        )

        return dtos.TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            access_expires=access_exp,
            refresh_expires=refresh_exp,
        )


class RefreshTokenUseCase(AuthUseCase):
    def __init__(
        self,
        auth_session_repository: repositories.AuthSessionRepository,
        token_service: services.TokenService,
    ):
        self.__auth_session_repository = auth_session_repository
        self.__token_service = token_service

    async def execute(
        self, request: dtos.RefreshTokenRequestDTO
    ) -> dtos.TokenResponseDTO:
        refresh_token_data = self.__token_service.verify_refresh_token(
            request.refresh_token
        )

        session = await self.__auth_session_repository.get(
            refresh_token_data.session_id
        )

        await self.__auth_session_repository.set_login(session.session_id)

        access_token, access_exp = self.__token_service.create_access_token(
            session.user_id, session.session_id
        )
        refresh_token, refresh_exp = self.__token_service.create_refresh_token(
            session.user_id, session.session_id
        )

        return dtos.TokenResponseDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            access_expires=access_exp,
            refresh_expires=refresh_exp,
        )


class AuthorizeUseCase(AuthUseCase):
    def __init__(
        self,
        auth_session_repository: repositories.AuthSessionRepository,
        token_service: services.TokenService,
    ):
        self.__auth_session_repository = auth_session_repository
        self.__token_service = token_service

    async def execute(
        self, request: dtos.AccessTokenRequestDTO
    ) -> dtos.UserResponseDTO:
        access_token_data = self.__token_service.verify_access_token(
            request.access_token
        )

        session = await self.__auth_session_repository.get(access_token_data.session_id)

        await self.__auth_session_repository.set_login(session.session_id)

        return dtos.UserResponseDTO(user_id=session.user_id)


class LogoutUseCase(AuthUseCase):
    def __init__(
        self,
        auth_session_repository: repositories.AuthSessionRepository,
        token_service: services.TokenService,
    ):
        self.__auth_session_repository = auth_session_repository
        self.__token_service = token_service

    async def execute(self, request: dtos.AccessTokenRequestDTO) -> None:
        access_token_data = self.__token_service.verify_access_token(
            request.access_token
        )

        session = await self.__auth_session_repository.get(access_token_data.session_id)

        await self.__auth_session_repository.set_login(session.session_id)

        await self.__auth_session_repository.delete(session.session_id)


class GetSessionsUseCase(AuthUseCase):
    def __init__(
        self,
        auth_session_repository: repositories.AuthSessionRepository,
    ):
        self.__auth_session_repository = auth_session_repository

    async def execute(
        self, request: dtos.SessionsRequestDTO
    ) -> dtos.SessionsResponseDTO:
        sessions = await self.__auth_session_repository.get_list(request.user_id)
        return dtos.SessionsResponseDTO.model_validate(sessions, from_attributes=True)
