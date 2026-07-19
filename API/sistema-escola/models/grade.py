from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    school_subject: Mapped[str] = mapped_column(String(100))
    grade: Mapped[float] = mapped_column()
    bimester: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
