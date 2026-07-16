from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class Convite(Base):
    __tablename__ = "convites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    usado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
