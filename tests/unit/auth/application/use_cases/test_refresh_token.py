import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src.auth.application.use_cases import RefreshTokenUseCase
from src.auth.application.dtos import RefreshTokenRequestDTO, TokenResponseDTO
from src.auth.domain.entities import AuthSession, AuthUser

@pytest.mark.asyncio
async def test_refresh_token_success(fake_user_repo, fake_session_repo, fake_token_service):
    user_id = uuid4()
    session_id = uuid4()
    email = "refresh@example.com"
    fake_token_service.user_id = user_id
    fake_token_service.session_id = session_id
    await fake_user_repo.create(AuthUser(
        id=user_id,
        email=email,
        password_hash="hash",
        created_at=datetime.now(timezone.utc),
        last_modified=datetime.now(timezone.utc),
    ))
    await fake_session_repo.create(AuthSession(
        session_id=session_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    ))
    refresh_token, _ = fake_token_service.create_refresh_token(user_id, session_id)
    use_case = RefreshTokenUseCase(fake_session_repo, fake_token_service)
    request = RefreshTokenRequestDTO(refresh_token=refresh_token)
    response = await use_case.execute(request)
    assert isinstance(response, TokenResponseDTO)
    assert response.access_token
    assert response.refresh_token
