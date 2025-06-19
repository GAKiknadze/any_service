from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


def create_async_engine_and_sessionmaker(database_url: str):
    engine = create_async_engine(database_url, echo=False, future=True)
    session_maker = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    return engine, session_maker
