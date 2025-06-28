import pytest

from src.auth.infrastructure.services import PasswordServiceImpl


@pytest.fixture
def password_service():
    return PasswordServiceImpl()


def test_hash_and_verify_password(password_service):
    password = "supersecret"
    hashed = password_service.hash_password(password)
    assert isinstance(hashed, str)
    assert hashed != password
    assert password_service.verify_password(password, hashed)


def test_verify_password_fail(password_service):
    password = "supersecret"
    wrong_password = "notsecret"
    hashed = password_service.hash_password(password)
    assert not password_service.verify_password(wrong_password, hashed)
