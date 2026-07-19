from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Invite(Base):
    __tablename__ = "invites"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    used: Mapped[bool] = mapped_column(default=False)
