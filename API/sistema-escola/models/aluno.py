from datetime import date
from typing import Optional

from sqlalchemy import String, ForeignKey, DATE, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String, nullable=False)
    data_nascimento: Mapped[date] = mapped_column(DATE, nullable=False)
    turma: Mapped[Optional[int]] = mapped_column(ForeignKey("turmas.id"))
    nome_responsavel: Mapped[str] = mapped_column(String, nullable=False)
    celular_responsavel: Mapped[str] = mapped_column(String, nullable=False)
    deletado: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, server_default="false"
    )
