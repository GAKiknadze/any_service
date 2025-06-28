import pytest
import uuid
from datetime import datetime, timezone

from src.auth.infrastructure.database.repositories import SQLAlchemyAuthSessionRepository
from src.auth.domain.entities import AuthSession
from src.auth.domain.exceptions import UserNotFoundExc

@pytest.fixture
def session_data():
    now = datetime.now(timezone.utc)
    return AuthSession(
        session_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        created_at=now,
        last_login=None,
    )

@pytest.mark.asyncio
async def test_create_and_get(session, session_data):
    repo = SQLAlchemyAuthSessionRepository(session)
    created = await repo.create(session_data)
    assert created.session_id == session_data.session_id
    assert created.user_id == session_data.user_id

    fetched = await repo.get(session_data.session_id)
    assert fetched.session_id == session_data.session_id
    assert fetched.user_id == session_data.user_id

@pytest.mark.asyncio
async def test_get_list(session, session_data):
    repo = SQLAlchemyAuthSessionRepository(session)
    await repo.create(session_data)
    sessions = await repo.get_list(session_data.user_id)
    assert any(s.session_id == session_data.session_id for s in sessions)

@pytest.mark.asyncio
async def test_set_login(session, session_data):
    repo = SQLAlchemyAuthSessionRepository(session)
    await repo.create(session_data)
    await repo.set_login(session_data.session_id)
    updated = await repo.get(session_data.session_id)
    assert updated.last_login is not None
    assert isinstance(updated.last_login, datetime)

@pytest.mark.asyncio
async def test_delete(session, session_data):
    repo = SQLAlchemyAuthSessionRepository(session)
    await repo.create(session_data)
    await repo.delete(session_data.session_id)
    with pytest.raises(UserNotFoundExc):
        await repo.get(session_data.session_id)

@pytest.mark.asyncio
async def test_get_not_found(session):
    repo = SQLAlchemyAuthSessionRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.get(uuid.uuid4())

@pytest.mark.asyncio
async def test_get_list_not_found(session):
    repo = SQLAlchemyAuthSessionRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.get_list(uuid.uuid4())

@pytest.mark.asyncio
async def test_set_login_not_found(session):
    repo = SQLAlchemyAuthSessionRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.set_login(uuid.uuid4())
