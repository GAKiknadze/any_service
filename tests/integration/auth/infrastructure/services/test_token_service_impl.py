import uuid
from datetime import timedelta

import pytest

from src.auth.domain.exceptions import InvalidCredentialsExc
from src.auth.infrastructure.services import TokenServiceImpl

SECRET_KEY = "testsecret"


@pytest.fixture
def token_service():
    return TokenServiceImpl(
        secret_key=SECRET_KEY,
        access_token_expire_minutes=1,
        refresh_token_expire_days=1,
    )


@pytest.fixture
def user_and_session_ids():
    return uuid.uuid4(), uuid.uuid4()


def test_create_and_verify_access_token(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    token, exp = token_service.create_access_token(user_id, session_id)
    assert isinstance(token, str)
    assert isinstance(exp, int)
    data = token_service.verify_access_token(token)
    assert data.user_id == user_id
    assert data.session_id == session_id


def test_create_and_verify_refresh_token(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    token, exp = token_service.create_refresh_token(user_id, session_id)
    assert isinstance(token, str)
    assert isinstance(exp, int)
    data = token_service.verify_refresh_token(token)
    assert data.user_id == user_id
    assert data.session_id == session_id


def test_access_token_wrong_type(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    token, _ = token_service.create_refresh_token(user_id, session_id)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_access_token(token)


def test_refresh_token_wrong_type(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    token, _ = token_service.create_access_token(user_id, session_id)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_refresh_token(token)


def test_access_token_invalid_signature(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    other_service = TokenServiceImpl(secret_key="wrongsecret")
    token, _ = other_service.create_access_token(user_id, session_id)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_access_token(token)


def test_refresh_token_invalid_signature(token_service, user_and_session_ids):
    user_id, session_id = user_and_session_ids
    other_service = TokenServiceImpl(secret_key="wrongsecret")
    token, _ = other_service.create_refresh_token(user_id, session_id)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_refresh_token(token)


def test_access_token_expired(token_service, user_and_session_ids, monkeypatch):
    user_id, session_id = user_and_session_ids
    # monkeypatch datetime to simulate expired token
    import src.auth.infrastructure.services as services

    real_datetime = services.datetime

    class FakeDatetime(real_datetime):
        @classmethod
        def now(cls, tz=None):
            return real_datetime.now(tz) - timedelta(minutes=10)

    monkeypatch.setattr(services, "datetime", FakeDatetime)
    token, _ = token_service.create_access_token(user_id, session_id)
    monkeypatch.setattr(services, "datetime", real_datetime)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_access_token(token)


def test_refresh_token_expired(token_service, user_and_session_ids, monkeypatch):
    user_id, session_id = user_and_session_ids
    import src.auth.infrastructure.services as services

    real_datetime = services.datetime

    class FakeDatetime(real_datetime):
        @classmethod
        def now(cls, tz=None):
            return real_datetime.now(tz) - timedelta(days=10)

    monkeypatch.setattr(services, "datetime", FakeDatetime)
    token, _ = token_service.create_refresh_token(user_id, session_id)
    monkeypatch.setattr(services, "datetime", real_datetime)
    with pytest.raises(InvalidCredentialsExc):
        token_service.verify_refresh_token(token)
