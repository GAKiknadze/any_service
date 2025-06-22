from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain import repositories, services
from src.auth.infrastructure.database.repositories import (
    SQLAlchemyAuthSessionRepository,
    SQLAlchemyAuthUserRepository,
)
from src.auth.infrastructure.services import PasswordServiceImpl, TokenServiceImpl


class AuthProvider(Provider):
    def __init__(self, secret_key: str):
        super().__init__()
        self.secret_key = secret_key

    @provide(scope=Scope.APP)
    async def _password_service(self) -> services.PasswordService:
        return PasswordServiceImpl()

    @provide(scope=Scope.APP)
    async def _token_service(self) -> services.TokenService:
        return TokenServiceImpl(secret_key=self.secret_key)

    @provide(scope=Scope.REQUEST)
    async def _auth_user_repo(
        self, session: AsyncSession
    ) -> repositories.AuthUserRepository:
        return SQLAlchemyAuthUserRepository(session)

    @provide(scope=Scope.REQUEST)
    async def _auth_session_repo(
        self, session: AsyncSession
    ) -> repositories.AuthSessionRepository:
        return SQLAlchemyAuthSessionRepository(session)
