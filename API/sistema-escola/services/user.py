from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.user_exceptions import (
    UserNotFound,
)
from models import Usuario


def get_user_by_id(id_user: int, session: Session) -> Usuario:
    user = session.execute(
        select(Usuario).where(Usuario.id == id_user)
    ).scalar_one_or_none()
    if not user:
        raise UserNotFound
    return user


def get_user_by_id_or_none(id_user: int, session: Session) -> Usuario | None:
    user = session.execute(
        select(Usuario).where(Usuario.id == id_user)
    ).scalar_one_or_none()
    if not user:
        return None
    return user


def get_user_by_email_or_none(email: int, session: Session) -> Usuario | None:
    user = session.execute(
        select(Usuario).where(Usuario.email == email)
    ).scalar_one_or_none()
    if not user:
        return None
    return user
