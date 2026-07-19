from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.user_exceptions import (
    UserNotFound,
)
from models import User


def get_user_by_id(user_id: int, session: Session) -> User:
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise UserNotFound
    return user


def get_user_by_id_or_none(user_id: int, session: Session) -> User | None:
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        return None
    return user


def get_user_by_email_or_none(email: str, session: Session) -> User | None:
    user = session.execute(select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        return None
    return user
