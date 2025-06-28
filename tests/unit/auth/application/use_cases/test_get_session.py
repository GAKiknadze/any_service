from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.auth.application.dtos import SessionsRequestDTO, SessionsResponseDTO
from src.auth.application.use_cases import GetSessionsUseCase
from src.auth.domain.entities import AuthSession


@pytest.mark.asyncio
async def test_get_sessions_success(fake_session_repo):
    user_id = uuid4()
    session1 = AuthSession(
        session_id=uuid4(),
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    session2 = AuthSession(
        session_id=uuid4(),
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await fake_session_repo.create(session1)
    await fake_session_repo.create(session2)
    use_case = GetSessionsUseCase(fake_session_repo)
    request = SessionsRequestDTO(user_id=user_id)
    response = await use_case.execute(request)
    assert isinstance(response, SessionsResponseDTO)  # type: ignore[misc]
    assert len(response.root) == 2
