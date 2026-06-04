from sqlalchemy import Column, Integer, ForeignKey, String, Float

from .base import Base

class Nota(Base):
    __tablename__ = "notas"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    aluno = Column(ForeignKey("alunos.id"), nullable=False)
    materia = Column(String(100), nullable=False)
    nota = Column(Float)
    bimestre = Column(Integer, nullable=False)
    ano = Column(Integer, nullable=False)