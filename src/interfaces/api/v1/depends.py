from uuid import UUID

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Cookie, Depends

from src.auth.application.dtos import AccessTokenRequestDTO
from src.auth.application.use_cases import AuthorizeUseCase
from src.auth.domain.exceptions import InvalidCredentialsExc


async def get_access_token(access_token: str | None = Cookie(None)) -> str:
    if access_token is None:
        raise InvalidCredentialsExc("empty access token")

    _, token = access_token.split(sep=" ", maxsplit=1)
    return token


@inject
async def get_user_id(
    use_case: FromDishka[AuthorizeUseCase],
    access_token: str = Depends(get_access_token),
) -> UUID:
    data = await use_case.execute(AccessTokenRequestDTO(access_token=access_token))
    return data.user_id
