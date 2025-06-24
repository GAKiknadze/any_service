import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database import Base


class UserInfo(Base):
    __tablename__ = "user_info"

    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    nick_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    avatar: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
