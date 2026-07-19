from sqlalchemy import select
from sqlalchemy.orm import Session

from core.crud import update_model
from core.authorization import verify_authorization
from exceptions.role_exceptions import PositionNotFound, PositionAlreadyExists
from models import User, Role, Log
from schemas.role import RoleSchema


def consult_position(role_id: int, session: Session, user: User) -> Role:
    role = session.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if not role:
        raise PositionNotFound
    log = Log(
        user_id=user.id,
        action="consult_role",
        description=f"Cargo {role.name}, de ID {role.id}, foi consultado.",
    )
    session.add(log)
    session.commit()
    return role


def register_position(role_schema: RoleSchema, session: Session, user: User) -> Role:
    verify_authorization(user)
    role = session.execute(
        select(Role).where(Role.name == role_schema.name)
    ).scalar_one_or_none()
    if role:
        raise PositionAlreadyExists
    new_role = Role(name=role_schema.name)
    session.add(new_role)
    session.flush()
    log = Log(
        user_id=user.id,
        action="register_role",
        description=f"Cargo {new_role.name}, de ID {new_role.id}, foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(new_role)
    return new_role


def delete_position(role_id: int, session: Session, user: User) -> Role:
    verify_authorization(user)
    role = session.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if not role:
        raise PositionNotFound
    session.delete(role)
    log = Log(
        user_id=user.id,
        action="delete_role",
        description=f"Cargo {role.name}, de ID {role.id}, foi deletado.",
    )
    session.add(log)
    session.commit()
    return role


def update_position(
    role_id: int, role_schema: RoleSchema, session: Session, user: User
) -> Role:
    verify_authorization(user)
    role = session.execute(select(Role).where(Role.id == role_id)).scalar_one_or_none()
    if not role:
        raise PositionNotFound
    update_model(obj=role, schema=role_schema)
    log = Log(
        user_id=user.id,
        action="update_role",
        description=f"Cargo {role.name}, de ID {role.id}, foi atualizado.",
    )
    session.add(log)
    session.commit()
    session.refresh(role)
    return role


def get_position_by_id_or_none(role_id: int, session: Session) -> Role | None:
    position = session.execute(
        select(Role).where(Role.id == role_id)
    ).scalar_one_or_none()
    return position
