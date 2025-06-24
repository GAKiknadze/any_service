from typing import List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.profile.domain.entities import UserInfo as DomainUserInfo
from .models import UserInfo as DBUserInfo


def _db_to_domain(db_user: DBUserInfo) -> DomainUserInfo:
    return DomainUserInfo(
        user_id=db_user.user_id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        nick_name=db_user.nick_name,
        date_of_birth=db_user.date_of_birth,
        avatar=db_user.avatar,
        created_at=db_user.created_at,
        updated_at=db_user.updated_at,
    )


class SQLAlchemyUserInfoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, value: DomainUserInfo) -> DomainUserInfo:
        db_user = DBUserInfo(
            user_id=value.user_id,
            first_name=value.first_name,
            last_name=value.last_name,
            nick_name=value.nick_name,
            date_of_birth=value.date_of_birth,
            avatar=value.avatar,
            created_at=value.created_at,
            updated_at=value.updated_at,
        )
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return _db_to_domain(db_user)

    async def get(self, user_id: UUID) -> DomainUserInfo:
        stmt = select(DBUserInfo).where(DBUserInfo.user_id == user_id)
        res = await self.session.execute(stmt)
        db_user = res.scalar_one_or_none()
        if db_user is None:
            raise ValueError(f"UserInfo with id {user_id} not found")
        return _db_to_domain(db_user)

    async def get_by_nick_name(self, value: str, offset: int = 0, limit: int = 50) -> List[DomainUserInfo]:
        stmt = (
            select(DBUserInfo)
            .where(DBUserInfo.nick_name == value)
            .offset(offset)
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        db_users = res.scalars().all()
        return [_db_to_domain(u) for u in db_users]

    async def update(self, value: DomainUserInfo) -> DomainUserInfo:
        stmt = select(DBUserInfo).where(DBUserInfo.user_id == value.user_id)
        res = await self.session.execute(stmt)
        db_user = res.scalar_one_or_none()
        if db_user is None:
            raise ValueError(f"UserInfo with id {value.user_id} not found")
        db_user.first_name = value.first_name
        db_user.last_name = value.last_name
        db_user.nick_name = value.nick_name
        db_user.date_of_birth = value.date_of_birth
        db_user.avatar = value.avatar
        db_user.created_at = value.created_at
        db_user.updated_at = value.updated_at
        await self.session.commit()
        await self.session.refresh(db_user)
        return _db_to_domain(db_user)
