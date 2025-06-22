from datetime import datetime, timedelta, timezone
from uuid import uuid4

from src.auth.domain import entities, exceptions


class FakeAuthUserRepository:
    def __init__(self):
        self.users = {}

    async def create(self, value: entities.AuthUser):
        self.users[value.email] = value
        self.users[value.id] = value
        return value

    async def update(self, user_id, new_email=None, new_password_hash=None):
        user = self.users.get(user_id)
        if not user:
            raise exceptions.UserNotFoundExc()
        if new_email:
            user.email = new_email
        if new_password_hash:
            user.password_hash = new_password_hash
        user.last_modified = datetime.now(timezone.utc)
        return user

    async def get_by_email(self, value):
        user = self.users.get(value)
        if not user:
            raise exceptions.UserNotFoundExc()
        return user

    async def get_by_id(self, value):
        user = self.users.get(value)
        if not user:
            raise exceptions.UserNotFoundExc()
        return user


class FakeAuthSessionRepository:
    def __init__(self):
        self.sessions = {}

    async def create(self, value: entities.AuthSession):
        self.sessions[value.session_id] = value
        return value

    async def get(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise exceptions.UserNotFoundExc()
        return session

    async def get_list(self, user_id):
        result = [s for s in self.sessions.values() if s.user_id == user_id]
        if not result:
            raise exceptions.UserNotFoundExc()
        return result

    async def set_login(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            raise exceptions.UserNotFoundExc()
        session.last_login = datetime.now(timezone.utc)

    async def delete(self, session_id):
        self.sessions.pop(session_id, None)


class FakePasswordService:
    def __init__(self):
        self._hash = "hashed"

    def verify_password(self, plain, hashed):
        return hashed == self._hash and plain == "password"

    def hash_password(self, password):
        return self._hash


class FakeTokenService:
    def __init__(self):
        self._access_token = "access"
        self._refresh_token = "refresh"
        self._user_id = uuid4()
        self._session_id = uuid4()

    def create_access_token(self, user_id, session_id):
        return (
            self._access_token,
            int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()),
        )

    def create_refresh_token(self, user_id, session_id):
        return (
            self._refresh_token,
            int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp()),
        )

    def verify_access_token(self, token):
        if token != self._access_token:
            raise exceptions.InvalidCredentialsExc()
        return entities.AccessTokenData(
            user_id=self._user_id, session_id=self._session_id
        )

    def verify_refresh_token(self, token):
        if token != self._refresh_token:
            raise exceptions.InvalidCredentialsExc()
        return entities.RefreshTokenData(
            user_id=self._user_id, session_id=self._session_id
        )
