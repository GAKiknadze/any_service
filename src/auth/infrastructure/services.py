from passlib.context import CryptContext
from jose import jwt, JWTError
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Tuple
from src.auth.domain.entities import AccessTokenData, RefreshTokenData


class PasswordServiceImpl:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self._pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str) -> str:
        return self._pwd_context.hash(password)


class TokenServiceImpl:
    def __init__(
        self,
        secret_key: str,
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 30,
        algorithm: str = "HS256",
    ):
        self.secret_key = secret_key
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days
        self.algorithm = algorithm

    def create_access_token(self, user_id: UUID, session_id: UUID) -> Tuple[str, int]:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "sid": str(session_id),
            "type": "access",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, int(expire.timestamp())

    def create_refresh_token(self, user_id: UUID, session_id: UUID) -> Tuple[str, int]:
        now = datetime.now(timezone.utc)
        expire = now + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "sid": str(session_id),
            "type": "refresh",
            "exp": int(expire.timestamp()),
            "iat": int(now.timestamp()),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, int(expire.timestamp())

    def verify_access_token(self, token: str) -> AccessTokenData:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "access":
                raise JWTError("Invalid token type")
            user_id = UUID(payload["sub"])
            session_id = UUID(payload["sid"])
            return AccessTokenData(user_id=user_id, session_id=session_id)
        except Exception as e:
            raise JWTError("Invalid access token") from e

    def verify_refresh_token(self, token: str) -> RefreshTokenData:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            if payload.get("type") != "refresh":
                raise JWTError("Invalid token type")
            user_id = UUID(payload["sub"])
            session_id = UUID(payload["sid"])
            return RefreshTokenData(user_id=user_id, session_id=session_id)
        except Exception as e:
            raise JWTError("Invalid refresh token") from e
