from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.application import dtos
from src.auth.application.use_cases import (
    DeleteSessionUseCase,
    GetSessionsUseCase,
    LoginUseCase,
    LogoutUseCase,
    RefreshTokenUseCase,
    RegisterUseCase,
)

from .depends import get_user_id

auth_router = APIRouter()


@auth_router.post("/login", response_model=dtos.TokenResponseDTO)
@inject
async def login(
    request: dtos.LoginRequestDTO,
    use_case: FromDishka[LoginUseCase],
):
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/register", response_model=dtos.TokenResponseDTO)
@inject
async def register(
    request: dtos.RegisterRequestDTO,
    use_case: FromDishka[RegisterUseCase],
):
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@auth_router.post("/refresh", response_model=dtos.TokenResponseDTO)
@inject
async def refresh(
    request: dtos.RefreshTokenRequestDTO,
    use_case: FromDishka[RefreshTokenUseCase],
):
    try:
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


@auth_router.post("/logout")
@inject
async def logout(
    request: dtos.AccessTokenRequestDTO,
    use_case: FromDishka[LogoutUseCase],
):
    try:
        await use_case.execute(request)
        return {"detail": "Logged out"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))


session_router = APIRouter()


@session_router.get("/", response_model=dtos.SessionsResponseDTO)
@inject
async def get_sessions_list(
    use_case: FromDishka[GetSessionsUseCase],
    user_id: UUID = Depends(get_user_id),
):
    try:
        request = dtos.SessionsRequestDTO(user_id=user_id)
        return await use_case.execute(request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@session_router.delete("/{session_id}")
@inject
async def delete_session_by_id(
    session_id: UUID,
    use_case: FromDishka[DeleteSessionUseCase],
    user_id: UUID = Depends(get_user_id),
):
    try:
        request = dtos.DeleteSessionRequestDTO(session_id=session_id)
        await use_case.execute(request)
        return {"detail": "Session deleted"}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
