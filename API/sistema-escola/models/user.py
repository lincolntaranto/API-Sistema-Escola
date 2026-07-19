from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from sqlalchemy import String, ForeignKey


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str] = mapped_column(String(100))
    admin: Mapped[bool] = mapped_column(default=False)
