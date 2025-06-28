from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.auth.application.dtos import LoginRequestDTO, TokenResponseDTO
from src.auth.application.use_cases import LoginUseCase
from src.auth.domain.entities import AuthUser


@pytest.mark.asyncio
async def test_login_success(
    fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
):
    user_id = uuid4()
    email = "test@example.com"
    password = "password"
    password_hash = fake_password_service.hash_password(password)
    await fake_user_repo.create(
        AuthUser(
            id=user_id,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )
    )

    use_case = LoginUseCase(
        fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
    )
    request = LoginRequestDTO(email=email, password=password)
    response = await use_case.execute(request)
    assert isinstance(response, TokenResponseDTO)
    assert response.access_token
    assert response.refresh_token


@pytest.mark.asyncio
async def test_login_invalid_password(
    fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
):
    user_id = uuid4()
    email = "test2@example.com"
    password = "password"
    password_hash = fake_password_service.hash_password(password)
    await fake_user_repo.create(
        AuthUser(
            id=user_id,
            email=email,
            password_hash=password_hash,
            created_at=datetime.now(timezone.utc),
            last_modified=datetime.now(timezone.utc),
        )
    )

    use_case = LoginUseCase(
        fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
    )
    request = LoginRequestDTO(email=email, password="wrongpassword")
    with pytest.raises(Exception):
        await use_case.execute(request)
