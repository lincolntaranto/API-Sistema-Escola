import enum

from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Turnos(enum.Enum):
    manha = "manhã"
    tarde = "tarde"
    noite = "noite"


class Turma(Base):
    __tablename__ = "turmas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    serie: Mapped[str] = mapped_column(String(20))
    ano: Mapped[int] = mapped_column()
    turno: Mapped[Turnos] = mapped_column(Enum(Turnos))
