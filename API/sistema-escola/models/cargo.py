from sqlalchemy import Column, Integer, String

from .base import Base

class Cargo(Base):
    __tablename__ = "cargos"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    nome = Column(String(50), nullable=False)