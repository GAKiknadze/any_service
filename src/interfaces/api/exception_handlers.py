from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.auth.domain.exceptions import (
    ContactAlreadyExistsExc,
    InvalidCredentialsExc,
    UserNotFoundExc,
)


# Common
async def any_exc_handler(req: Request, exc: Exception):
    return JSONResponse(
        content={"msg": "something wrong"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


# Auth
async def contact_already_exists_exc_handler(
    req: Request, exc: ContactAlreadyExistsExc
):
    return JSONResponse(
        content={"msg": "contact already exists"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


async def invalid_credentials_exc_handler(req: Request, exc: InvalidCredentialsExc):
    return JSONResponse(
        content={"msg": "invalid credentials"}, status_code=status.HTTP_401_UNAUTHORIZED
    )


async def user_not_found_exc_handler(req: Request, exc: UserNotFoundExc):
    return JSONResponse(
        content={"msg": "user not found"}, status_code=status.HTTP_404_NOT_FOUND
    )
