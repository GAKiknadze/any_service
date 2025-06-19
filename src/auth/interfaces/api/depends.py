from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Cookie, HTTPException, status

from src.auth.application.dtos import AccessTokenRequestDTO
from src.auth.application.use_cases import AuthorizeUseCase


@inject
async def get_user_id(
    use_case: FromDishka[AuthorizeUseCase], access_token: str | None = Cookie(None)
) -> UUID:
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data = await use_case.execute(AccessTokenRequestDTO(access_token=access_token))
    return data.user_id
