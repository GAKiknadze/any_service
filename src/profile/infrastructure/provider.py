from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile.domain.repositories import UserInfoRepository
from src.profile.infrastructure.database.repositories import (
    SQLAlchemyUserInfoRepository,
)


class ProfileProvider(Provider):
    def __init__(self):
        super().__init__()

    @provide(scope=Scope.REQUEST)
    async def _user_info_repo(self, session: AsyncSession) -> UserInfoRepository:
        return SQLAlchemyUserInfoRepository(session)
