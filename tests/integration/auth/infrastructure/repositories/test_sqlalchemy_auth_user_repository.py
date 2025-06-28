import pytest
import uuid
from datetime import datetime, timezone

from src.auth.infrastructure.database.repositories import SQLAlchemyAuthUserRepository
from src.auth.domain.entities import AuthUser
from src.auth.domain.exceptions import UserNotFoundExc


@pytest.fixture
def user():
    now = datetime.now(timezone.utc)
    return AuthUser(
        id=uuid.uuid4(),
        email="test@example.com",
        password_hash="hashedpassword",
        created_at=now,
        last_modified=now,
    )

@pytest.mark.asyncio
async def test_create_and_get_by_id(session, user):
    repo = SQLAlchemyAuthUserRepository(session)
    created = await repo.create(user)
    assert created.id == user.id
    assert created.email == user.email

    fetched = await repo.get_by_id(user.id)
    assert fetched.email == user.email
    assert fetched.password_hash == user.password_hash

@pytest.mark.asyncio
async def test_get_by_email(session, user):
    repo = SQLAlchemyAuthUserRepository(session)
    await repo.create(user)
    fetched = await repo.get_by_email(user.email)
    assert fetched.id == user.id

@pytest.mark.asyncio
async def test_update_email_and_password(session, user):
    repo = SQLAlchemyAuthUserRepository(session)
    await repo.create(user)
    new_email = "new@example.com"
    new_password = "newhash"
    updated = await repo.update(user_id=user.id, new_email=new_email, new_password_hash=new_password)
    assert updated.email == new_email
    assert updated.password_hash == new_password

@pytest.mark.asyncio
async def test_get_by_id_not_found(session):
    repo = SQLAlchemyAuthUserRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.get_by_id(uuid.uuid4())

@pytest.mark.asyncio
async def test_get_by_email_not_found(session):
    repo = SQLAlchemyAuthUserRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.get_by_email("notfound@example.com")

@pytest.mark.asyncio
async def test_update_not_found(session):
    repo = SQLAlchemyAuthUserRepository(session)
    with pytest.raises(UserNotFoundExc):
        await repo.update(user_id=uuid.uuid4(), new_email="a@b.com")
