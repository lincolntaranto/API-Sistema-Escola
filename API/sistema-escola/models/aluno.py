from sqlalchemy import Column, Integer, String, ForeignKey, DATE, Boolean

from .base import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String, nullable=False)
    data_nascimento = Column(DATE, nullable=False)
    turma = Column(ForeignKey("turmas.id"))
    nome_responsavel = Column(String, nullable=False)
    celular_responsavel = Column(String, nullable=False)
    deletado = Column(Boolean, default=False, nullable=False)