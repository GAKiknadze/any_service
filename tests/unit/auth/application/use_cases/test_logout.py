from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.auth.application.dtos import AccessTokenRequestDTO
from src.auth.application.use_cases import LogoutUseCase
from src.auth.domain.entities import AuthSession, AuthUser


@pytest.mark.asyncio
async def test_logout_success(fake_user_repo, fake_session_repo, fake_token_service):
    user_id = uuid4()
    session_id = uuid4()
    email = "logout@example.com"
    fake_token_service.user_id = user_id
    fake_token_service.session_id = session_id
    await fake_user_repo.create(
        AuthUser(
            id=user_id,
            email=email,
            password_hash="hash",
            created_at=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )
    )
    await fake_session_repo.create(
        AuthSession(
            session_id=session_id,
            user_id=user_id,
            created_at=datetime.now(timezone.utc),
            last_login=datetime.now(timezone.utc),
        )
    )
    access_token, _ = fake_token_service.create_access_token(user_id, session_id)
    use_case = LogoutUseCase(fake_session_repo, fake_token_service)
    request = AccessTokenRequestDTO(access_token=access_token)
    await use_case.execute(request)
    assert session_id not in fake_session_repo.sessions
