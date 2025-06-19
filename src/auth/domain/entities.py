from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class AuthUser:
    id: UUID
    email: str
    password_hash: str
    created_at: datetime
    last_modified: datetime


@dataclass
class AuthSession:
    session_id: UUID
    user_id: UUID
    created_at: datetime
    last_login: datetime | None = None


@dataclass
class AccessTokenData:
    user_id: UUID
    session_id: UUID


@dataclass
class RefreshTokenData:
    user_id: UUID
    session_id: UUID
