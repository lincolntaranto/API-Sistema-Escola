import enum

from sqlalchemy import Column, Integer, String, Enum

from .base import Base


class Turnos(enum.Enum):
    manha = "manhã"
    tarde = "tarde"
    noite = "noite"


class Turma(Base):
    __tablename__ = "turmas"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(100), nullable=False)
    serie = Column(String(20), nullable=False)
    ano = Column(Integer, nullable=False)
    turno = Column(Enum(Turnos), nullable=False)
