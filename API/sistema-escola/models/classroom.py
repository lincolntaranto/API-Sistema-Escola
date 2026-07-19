import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Shifts(enum.Enum):
    morning = "morning"
    afternoon = "afternoon"
    night = "night"


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    school_year: Mapped[str] = mapped_column(String(20))
    year: Mapped[int] = mapped_column()
    shift: Mapped[Shifts] = mapped_column(Enum(Shifts))
