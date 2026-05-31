from datetime import datetime, timezone

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from .base import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_usuario = Column(ForeignKey("usuarios.id"), nullable=False)
    id_aluno = Column(ForeignKey("alunos.id"))
    acao = Column(String(100), nullable=False)
    descricao = Column(String(100), nullable=True)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)