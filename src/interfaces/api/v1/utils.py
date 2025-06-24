from fastapi.responses import JSONResponse

from src.auth.application.dtos import TokenResponseDTO

from .schemas.auth import TokenResponse


def create_new_tokens_response(tokens: TokenResponseDTO) -> JSONResponse:
    response = JSONResponse(
        content=TokenResponse(
            access_token=tokens.access_token, access_token_type=tokens.token_type
        )
    )

    response.set_cookie(
        "refresh_token",
        tokens.refresh_token,
        expires=tokens.refresh_expires,
        secure=True,
    )

    return response
