import pytest
from uuid import uuid4
from datetime import datetime, timezone

from src.auth.application.use_cases import DeleteSessionUseCase
from src.auth.application.dtos import DeleteSessionRequestDTO
from src.auth.domain.entities import AuthSession

@pytest.mark.asyncio
async def test_delete_session_success(fake_session_repo):
    user_id = uuid4()
    session_id = uuid4()
    session = AuthSession(
        session_id=session_id,
        user_id=user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await fake_session_repo.create(session)
    use_case = DeleteSessionUseCase(fake_session_repo)
    request = DeleteSessionRequestDTO(session_id=session_id)
    await use_case.execute(request)
    assert session_id not in fake_session_repo.sessions
