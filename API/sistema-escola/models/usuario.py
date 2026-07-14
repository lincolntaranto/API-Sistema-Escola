from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha = Column(String(100), nullable=False)
    cargo = Column(ForeignKey("cargos.id"), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    numero = Column(String(100), nullable=False)
    admin = Column(Boolean, default=False, nullable=False)
