import pytest

from src.auth.domain.repositories import AuthSessionRepository, AuthUserRepository
from src.auth.domain.services import PasswordService, TokenService
from tests.unit.auth.application.fakes import (
    FakeAuthSessionRepository,
    FakeAuthUserRepository,
    FakePasswordService,
    FakeTokenService,
)


@pytest.fixture
def fake_user_repo() -> AuthUserRepository:
    return FakeAuthUserRepository()


@pytest.fixture
def fake_session_repo() -> AuthSessionRepository:
    return FakeAuthSessionRepository()


@pytest.fixture
def fake_password_service() -> PasswordService:
    return FakePasswordService()


@pytest.fixture
def fake_token_service() -> TokenService:
    return FakeTokenService()
