import pytest
from uuid import uuid4

from src.auth.application.use_cases import RegisterUseCase
from src.auth.application.dtos import RegisterRequestDTO, TokenResponseDTO

@pytest.mark.asyncio
async def test_register_success(fake_user_repo, fake_session_repo, fake_password_service, fake_token_service):
    user_id = uuid4()
    email = "newuser@example.com"
    password = "newpassword"
    use_case = RegisterUseCase(
        fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
    )
    request = RegisterRequestDTO(user_id=user_id, email=email, password=password)
    response = await use_case.execute(request)
    assert isinstance(response, TokenResponseDTO)
    assert response.access_token
    assert response.refresh_token

@pytest.mark.asyncio
async def test_register_existing_email(fake_user_repo, fake_session_repo, fake_password_service, fake_token_service):
    user_id = uuid4()
    email = "existing@example.com"
    password = "password"
    # Register first time
    use_case = RegisterUseCase(
        fake_user_repo, fake_session_repo, fake_password_service, fake_token_service
    )
    request = RegisterRequestDTO(user_id=user_id, email=email, password=password)
    await use_case.execute(request)
    # Try to register again
    with pytest.raises(Exception):
        await use_case.execute(request)
