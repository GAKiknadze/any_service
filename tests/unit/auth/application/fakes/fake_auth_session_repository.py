from datetime import datetime, timezone

from src.auth.domain import entities, exceptions

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
