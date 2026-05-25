from passlib.handlers.bcrypt import bcrypt

from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(100), nullable=False)
    senha = Column(String(50), nullable=False)
    cargo = Column(ForeignKey("cargos.id"), nullable=False)
    email = Column(String(100), nullable=False)
    numero = Column(String(100), nullable=False)
