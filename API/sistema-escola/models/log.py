from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    student_id: Mapped[Optional[int]] = mapped_column(ForeignKey("students.id"))
    action: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(100))
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
