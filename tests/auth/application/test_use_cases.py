import asyncio
from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.auth.application import dtos, use_cases
from src.auth.domain import entities, exceptions

from .fakes import (
    FakeAuthSessionRepository,
    FakeAuthUserRepository,
    FakePasswordService,
    FakeTokenService,
)


@pytest.fixture
def user_repo():
    return FakeAuthUserRepository()


@pytest.fixture
def session_repo():
    return FakeAuthSessionRepository()


@pytest.fixture
def password_service():
    return FakePasswordService()


@pytest.fixture
def token_service():
    return FakeTokenService()


@pytest.fixture
def user(user_repo, password_service):
    user = entities.AuthUser(
        id=uuid4(),
        email="test@example.com",
        password_hash=password_service.hash_password("password"),
        created_at=datetime.now(timezone.utc),
        last_modified=datetime.now(timezone.utc),
    )
    asyncio.get_event_loop().run_until_complete(user_repo.create(user))
    return user


@pytest.fixture
def session(session_repo, user):
    session = entities.AuthSession(
        session_id=uuid4(),
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    asyncio.get_event_loop().run_until_complete(session_repo.create(session))
    return session


@pytest.mark.asyncio
async def test_login_success(
    user_repo, session_repo, password_service, token_service, user
):
    uc = use_cases.LoginUseCase(
        user_repo, session_repo, password_service, token_service
    )
    req = dtos.LoginRequestDTO(email=user.email, password="password")
    resp = await uc.execute(req)
    assert resp.access_token == token_service._access_token
    assert resp.refresh_token == token_service._refresh_token


@pytest.mark.asyncio
async def test_login_invalid_password(
    user_repo, session_repo, password_service, token_service, user
):
    uc = use_cases.LoginUseCase(
        user_repo, session_repo, password_service, token_service
    )
    req = dtos.LoginRequestDTO(email=user.email, password="wrong")
    with pytest.raises(exceptions.InvalidCredentialsExc):
        await uc.execute(req)


@pytest.mark.asyncio
async def test_register_success(
    user_repo, session_repo, password_service, token_service
):
    uc = use_cases.RegisterUseCase(
        user_repo, session_repo, password_service, token_service
    )
    req = dtos.RegisterRequestDTO(email="new@example.com", password="password")
    resp = await uc.execute(req)
    assert resp.access_token == token_service._access_token


@pytest.mark.asyncio
async def test_register_duplicate(
    user_repo, session_repo, password_service, token_service, user
):
    uc = use_cases.RegisterUseCase(
        user_repo, session_repo, password_service, token_service
    )
    req = dtos.RegisterRequestDTO(email=user.email, password="password")
    with pytest.raises(exceptions.ContactAlreadyExistsExc):
        await uc.execute(req)


@pytest.mark.asyncio
async def test_refresh_token_success(session_repo, token_service):
    uc = use_cases.RefreshTokenUseCase(session_repo, token_service)

    session = entities.AuthSession(
        session_id=token_service._session_id,
        user_id=token_service._user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await session_repo.create(session)
    req = dtos.RefreshTokenRequestDTO(refresh_token=token_service._refresh_token)
    resp = await uc.execute(req)
    assert resp.access_token == token_service._access_token


@pytest.mark.asyncio
async def test_refresh_token_invalid(session_repo, token_service):
    uc = use_cases.RefreshTokenUseCase(session_repo, token_service)
    req = dtos.RefreshTokenRequestDTO(refresh_token="bad")
    with pytest.raises(exceptions.InvalidCredentialsExc):
        await uc.execute(req)


@pytest.mark.asyncio
async def test_authorize_success(session_repo, token_service):
    uc = use_cases.AuthorizeUseCase(session_repo, token_service)
    session = entities.AuthSession(
        session_id=token_service._session_id,
        user_id=token_service._user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await session_repo.create(session)
    req = dtos.AccessTokenRequestDTO(access_token=token_service._access_token)
    resp = await uc.execute(req)
    assert resp.user_id == token_service._user_id


@pytest.mark.asyncio
async def test_logout_success(session_repo, token_service):
    uc = use_cases.LogoutUseCase(session_repo, token_service)
    session = entities.AuthSession(
        session_id=token_service._session_id,
        user_id=token_service._user_id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await session_repo.create(session)
    req = dtos.AccessTokenRequestDTO(access_token=token_service._access_token)
    await uc.execute(req)

    with pytest.raises(exceptions.UserNotFoundExc):
        await session_repo.get(token_service._session_id)


@pytest.mark.asyncio
async def test_get_sessions_success(session_repo, user):
    uc = use_cases.GetSessionsUseCase(session_repo)

    s1 = entities.AuthSession(
        session_id=uuid4(),
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    s2 = entities.AuthSession(
        session_id=uuid4(),
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await session_repo.create(s1)
    await session_repo.create(s2)
    req = dtos.SessionsRequestDTO(user_id=user.id)
    resp = await uc.execute(req)
    assert len(resp.sessions) >= 2


@pytest.mark.asyncio
async def test_delete_session_success(session_repo, user):
    uc = use_cases.DeleteSessionUseCase(session_repo)
    s = entities.AuthSession(
        session_id=uuid4(),
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
    )
    await session_repo.create(s)
    req = dtos.DeleteSessionRequestDTO(session_id=s.session_id)
    await uc.execute(req)
    with pytest.raises(exceptions.UserNotFoundExc):
        await session_repo.get(s.session_id)
        await uc.execute(req)
