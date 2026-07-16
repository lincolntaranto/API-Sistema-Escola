from datetime import date
from typing import Optional

from sqlalchemy import ForeignKey, DATE
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column()
    data_nascimento: Mapped[date] = mapped_column(DATE)
    turma: Mapped[Optional[int]] = mapped_column(ForeignKey("turmas.id"))
    nome_responsavel: Mapped[str] = mapped_column()
    celular_responsavel: Mapped[str] = mapped_column()
    deletado: Mapped[bool] = mapped_column(default=False, server_default="false")
