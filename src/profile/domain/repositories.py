from typing import List, Protocol
from uuid import UUID

from .entities import UserInfo


class UserInfoRepository(Protocol):
    async def create(self, value: UserInfo) -> UserInfo: ...

    async def get(self, user_id: UUID) -> UserInfo: ...

    async def get_by_nick_name(
        self, value: str, offset: int = 0, limit: int = 50
    ) -> List[UserInfo]: ...

    async def update(self, value: UserInfo) -> UserInfo: ...
