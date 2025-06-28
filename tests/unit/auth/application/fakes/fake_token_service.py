from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

from src.auth.domain import entities, exceptions


class FakeTokenService:
    def __init__(self):
        self.access_token = "access"
        self.refresh_token = "refresh"
        self.user_id = uuid4()
        self.session_id = uuid4()

    def create_access_token(self, user_id: UUID, session_id: UUID):
        return (
            self.access_token,
            int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()),
        )

    def create_refresh_token(self, user_id: UUID, session_id: UUID):
        return (
            self.refresh_token,
            int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp()),
        )

    def verify_access_token(self, token):
        if token != self.access_token:
            raise exceptions.InvalidCredentialsExc()
        return entities.AccessTokenData(
            user_id=self.user_id, session_id=self.session_id
        )

    def verify_refresh_token(self, token):
        if token != self.refresh_token:
            raise exceptions.InvalidCredentialsExc()
        return entities.RefreshTokenData(
            user_id=self.user_id, session_id=self.session_id
        )
