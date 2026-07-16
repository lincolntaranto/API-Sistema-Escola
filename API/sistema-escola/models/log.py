from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    id_aluno: Mapped[Optional[int]] = mapped_column(ForeignKey("alunos.id"))
    acao: Mapped[str] = mapped_column(String(100))
    descricao: Mapped[Optional[str]] = mapped_column(String(100))
    data_hora: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )
