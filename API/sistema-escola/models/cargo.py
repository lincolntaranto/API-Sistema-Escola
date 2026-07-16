from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Cargo(Base):
    __tablename__ = "cargos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(50), nullable=False)
