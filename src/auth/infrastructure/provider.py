from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.infrastructure.services import PasswordServiceImpl, TokenServiceImpl
from src.auth.infrastructure.database.repositories import (
    SQLAlchemyAuthUserRepository,
    SQLAlchemyAuthSessionRepository,
)


class AuthProvider(Provider):
    def __init__(self, secret_key: str):
        super().__init__()
        self.secret_key = secret_key

        self.provide(self._password_service, scope=Scope.APP)
        self.provide(self._token_service, scope=Scope.APP)
        self.provide(self._auth_user_repo, scope=Scope.REQUEST)
        self.provide(self._auth_session_repo, scope=Scope.REQUEST)

    @provide
    def _password_service(self) -> PasswordServiceImpl:
        return PasswordServiceImpl()

    @provide
    def _token_service(self) -> TokenServiceImpl:
        return TokenServiceImpl(secret_key=self.secret_key)

    @provide
    def _auth_user_repo(self, session: AsyncSession) -> SQLAlchemyAuthUserRepository:
        return SQLAlchemyAuthUserRepository(session)

    @provide
    def _auth_session_repo(
        self, session: AsyncSession
    ) -> SQLAlchemyAuthSessionRepository:
        return SQLAlchemyAuthSessionRepository(session)
