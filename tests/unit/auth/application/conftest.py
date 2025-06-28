import pytest

from tests.unit.auth.application.fakes import (
    FakeAuthUserRepository,
    FakeAuthSessionRepository,
    FakePasswordService,
    FakeTokenService,
)
from src.auth.domain.repositories import AuthSessionRepository, AuthUserRepository
from src.auth.domain.services import TokenService, PasswordService

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
