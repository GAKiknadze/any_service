from typing import List, Protocol
from uuid import UUID

from .entities import AuthSession, AuthUser


class AuthUserRepository(Protocol):
    async def create(self, value: AuthUser) -> AuthUser: ...

    async def update(
        self,
        user_id: UUID,
        new_email: str | None = None,
        new_password_hash: str | None = None,
    ) -> AuthUser: ...

    async def get_by_email(self, value: str) -> AuthUser: ...

    async def get_by_id(self, value: UUID) -> AuthUser: ...


class AuthSessionRepository(Protocol):
    async def create(self, value: AuthSession) -> AuthSession: ...

    async def get(self, session_id: UUID) -> AuthSession: ...

    async def get_list(self, user_id: UUID) -> List[AuthSession]: ...

    async def set_login(self, session_id: UUID) -> None: ...

    async def delete(self, session_id: UUID) -> None: ...
