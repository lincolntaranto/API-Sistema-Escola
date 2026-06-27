from sqlalchemy.orm import sessionmaker
from .base import db

SessionLocal = sessionmaker(bind=db)


def get_session():
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
