from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Cookie, Depends, status
from fastapi.responses import JSONResponse

from src.auth.application import dtos
from src.auth.application.use_cases import (
    DeleteSessionUseCase,
    GetSessionsUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
)
from src.auth.domain.exceptions import InvalidCredentialsExc

from .depends import get_access_token, get_user_id
from .schemas import TokenResponse
from .utils import create_new_tokens_response

auth_router = APIRouter()


@auth_router.post(
    "/login", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
@inject
async def login(
    request: dtos.LoginRequestDTO,
    use_case: FromDishka[LoginUseCase],
):
    tokens = await use_case.execute(request)

    return create_new_tokens_response(tokens)


@auth_router.post(
    "/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED
)
@inject
async def register(
    request: dtos.RegisterRequestDTO,
    use_case: FromDishka[RegisterUseCase],
):
    tokens = await use_case.execute(request)

    return create_new_tokens_response(tokens)


@auth_router.post(
    "/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK
)
@inject
async def refresh(
    use_case: FromDishka[RefreshTokenUseCase],
    refresh_token: str | None = Cookie(None),
):
    if refresh_token is None:
        raise InvalidCredentialsExc("empty refresh token")

    tokens = await use_case.execute(
        dtos.RefreshTokenRequestDTO(refresh_token=refresh_token)
    )

    return create_new_tokens_response(tokens)


@auth_router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def logout(
    use_case: FromDishka[LogoutUseCase], access_token: str = Depends(get_access_token)
):
    await use_case.execute(dtos.AccessTokenRequestDTO(access_token=access_token))
    return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)


session_router = APIRouter()


@session_router.get(
    "/", response_model=dtos.SessionsResponseDTO, status_code=status.HTTP_200_OK
)
@inject
async def get_sessions_list(
    use_case: FromDishka[GetSessionsUseCase],
    user_id: UUID = Depends(get_user_id),
):
    request = dtos.SessionsRequestDTO(user_id=user_id)
    return await use_case.execute(request)


@session_router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_session_by_id(
    session_id: UUID,
    use_case: FromDishka[DeleteSessionUseCase],
    _: UUID = Depends(get_user_id),
):
    request = dtos.DeleteSessionRequestDTO(session_id=session_id)
    await use_case.execute(request)
    return JSONResponse(content={}, status_code=status.HTTP_204_NO_CONTENT)
