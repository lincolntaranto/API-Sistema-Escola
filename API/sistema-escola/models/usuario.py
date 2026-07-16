from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from sqlalchemy import String, ForeignKey


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100))
    senha: Mapped[str] = mapped_column(String(100))
    cargo: Mapped[int] = mapped_column(ForeignKey("cargos.id"))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    numero: Mapped[str] = mapped_column(String(100))
    admin: Mapped[bool] = mapped_column(default=False)
