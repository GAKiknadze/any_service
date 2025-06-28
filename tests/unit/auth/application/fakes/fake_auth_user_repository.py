from datetime import datetime, timezone

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