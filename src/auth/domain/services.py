from typing import Protocol, Tuple
from uuid import UUID

from .entities import AccessTokenData, RefreshTokenData


class PasswordService(Protocol):
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...

    def hash_password(self, password: str) -> str: ...


class TokenService(Protocol):
    def create_access_token(
        self, user_id: UUID, session_id: UUID
    ) -> Tuple[str, int]: ...

    def create_refresh_token(
        self, user_id: UUID, session_id: UUID
    ) -> Tuple[str, int]: ...

    def verify_access_token(self, token: str) -> AccessTokenData: ...

    def verify_refresh_token(self, token: str) -> RefreshTokenData: ...
