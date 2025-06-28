from datetime import datetime, timezone
from typing import List
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain.entities import AuthSession as DomainAuthSession
from src.auth.domain.entities import AuthUser as DomainAuthUser
from src.auth.domain.exceptions import UserNotFoundExc

from .models import AuthSession as DBAuthSession
from .models import AuthUser as DBAuthUser


def _dbuser_to_domain(db_user: DBAuthUser) -> DomainAuthUser:
    return DomainAuthUser(
        id=db_user.id,
        email=db_user.email,
        password_hash=db_user.password_hash,
        created_at=db_user.created_at,
        last_modified=db_user.last_modified,
    )


def _dbsession_to_domain(db_session: DBAuthSession) -> DomainAuthSession:
    return DomainAuthSession(
        session_id=db_session.session_id,
        user_id=db_session.user_id,
        created_at=db_session.created_at,
        last_login=db_session.last_login,
    )


class SQLAlchemyAuthUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, value: DomainAuthUser) -> DomainAuthUser:
        db_user = DBAuthUser(
            id=value.id,
            email=value.email,
            password_hash=value.password_hash,
            created_at=value.created_at,
            last_modified=value.last_modified,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return _dbuser_to_domain(db_user)

    async def update(
        self,
        user_id: UUID,
        new_email: str | None = None,
        new_password_hash: str | None = None,
    ) -> DomainAuthUser:
        stmt = select(DBAuthUser).where(DBAuthUser.id == user_id)
        res = await self.session.execute(stmt)
        db_user = res.scalar_one_or_none()
        if db_user is None:
            raise UserNotFoundExc(f"User with id {user_id} not found")
        if new_email is not None:
            db_user.email = new_email
        if new_password_hash is not None:
            db_user.password_hash = new_password_hash
        db_user.last_modified = datetime.now(timezone.utc)
        await self.session.commit()
        await self.session.refresh(db_user)
        return _dbuser_to_domain(db_user)

    async def get_by_email(self, value: str) -> DomainAuthUser:
        stmt = select(DBAuthUser).where(DBAuthUser.email == value)
        res = await self.session.execute(stmt)
        db_user = res.scalar_one_or_none()
        if db_user is None:
            raise UserNotFoundExc(f"User with email {value} not found")
        return _dbuser_to_domain(db_user)

    async def get_by_id(self, value: UUID) -> DomainAuthUser:
        stmt = select(DBAuthUser).where(DBAuthUser.id == value)
        res = await self.session.execute(stmt)
        db_user = res.scalar_one_or_none()
        if db_user is None:
            raise UserNotFoundExc(f"User with id {value} not found")
        return _dbuser_to_domain(db_user)


class SQLAlchemyAuthSessionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, value: DomainAuthSession) -> DomainAuthSession:
        db_session = DBAuthSession(
            session_id=value.session_id,
            user_id=value.user_id,
            created_at=value.created_at,
            last_login=value.last_login,
        )
        self.session.add(db_session)
        await self.session.commit()
        await self.session.refresh(db_session)
        return _dbsession_to_domain(db_session)

    async def get(self, session_id: UUID) -> DomainAuthSession:
        stmt = select(DBAuthSession).where(DBAuthSession.session_id == session_id)
        res = await self.session.execute(stmt)
        db_session = res.scalar_one_or_none()
        if db_session is None:
            raise UserNotFoundExc(f"Session with id {session_id} not found")
        return _dbsession_to_domain(db_session)

    async def get_list(self, user_id: UUID) -> List[DomainAuthSession]:
        stmt = select(DBAuthSession).where(DBAuthSession.user_id == user_id)
        res = await self.session.execute(stmt)
        db_sessions = res.scalars().all()
        if not db_sessions:
            raise UserNotFoundExc(f"No sessions found for user {user_id}")
        return [_dbsession_to_domain(s) for s in db_sessions]

    async def set_login(self, session_id: UUID) -> None:
        stmt = select(DBAuthSession).where(DBAuthSession.session_id == session_id)
        res = await self.session.execute(stmt)
        db_session = res.scalar_one_or_none()
        if db_session is None:
            raise UserNotFoundExc(f"Session with id {session_id} not found")
        db_session.last_login = datetime.now(timezone.utc)
        await self.session.commit()

    async def delete(self, session_id: UUID) -> None:
        stmt = delete(DBAuthSession).where(DBAuthSession.session_id == session_id)
        await self.session.execute(stmt)
        await self.session.commit()
