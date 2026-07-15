from sqlalchemy import ForeignKey, String, Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Nota(Base):
    __tablename__ = "notas"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    id_aluno: Mapped[int] = mapped_column(ForeignKey("alunos.id"), nullable=False)
    materia: Mapped[str] = mapped_column(String(100), nullable=False)
    nota: Mapped[Float] = mapped_column(Float)
    bimestre: Mapped[int] = mapped_column(nullable=False)
    ano: Mapped[int] = mapped_column(nullable=False)
