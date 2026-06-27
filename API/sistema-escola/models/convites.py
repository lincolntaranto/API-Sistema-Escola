from sqlalchemy import Column, Integer, Boolean

from models import Base


class Convite(Base):
    __tablename__ = "convites"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    usado = Column(Boolean, default=False, nullable=False)
