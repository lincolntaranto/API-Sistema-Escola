from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, DATE
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    birth_date: Mapped[date] = mapped_column(DATE)
    classroom: Mapped[Optional[int]] = mapped_column(ForeignKey("classrooms.id"))
    parents_name: Mapped[str] = mapped_column()
    guardian_phone: Mapped[str] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False, server_default="false")
