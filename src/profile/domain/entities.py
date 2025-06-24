from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass
class UserInfo:
    user_id: UUID
    first_name: str
    last_name: str
    nick_name: str
    date_of_birth: date
    avatar: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
