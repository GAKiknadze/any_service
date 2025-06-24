from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.auth.application import dtos
from src.auth.application.use_cases import DeleteSessionUseCase, GetSessionsUseCase

from ..depends import get_user_id

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
