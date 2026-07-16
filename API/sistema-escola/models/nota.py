from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Nota(Base):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    id_aluno: Mapped[int] = mapped_column(ForeignKey("alunos.id"))
    materia: Mapped[str] = mapped_column(String(100))
    nota: Mapped[float] = mapped_column()
    bimestre: Mapped[int] = mapped_column()
    ano: Mapped[int] = mapped_column()
