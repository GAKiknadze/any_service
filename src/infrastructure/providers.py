from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from .database import create_async_engine_and_sessionmaker


class DatabaseProvider(Provider):
    def __init__(self, database_url: str):
        super().__init__()
        self.engine, self.session_maker = create_async_engine_and_sessionmaker(
            database_url
        )

    @provide(scope=Scope.REQUEST, provides=AsyncSession)
    async def _session(self) -> AsyncIterable[AsyncSession]:
        async with self.session_maker() as session:
            yield session
