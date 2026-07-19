import jwt
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.authorization import verify_authorization, create_invite
from core.config import settings
from core.security import ALGORITHM
from exceptions.role_exceptions import PositionNotFound
from exceptions.invite_exceptions import UsedInvitation, InvalidInvite
from models import User, Invite, Role, Log
from schemas.invite import InviteSchema
from services.role import get_position_by_id_or_none


def register_invite(invite_schema: InviteSchema, session: Session, user: User) -> str:
    verify_authorization(user)
    role = session.execute(
        select(Role).where(Role.id == invite_schema.role_id)
    ).scalar_one_or_none()
    if not role:
        raise PositionNotFound
    new_invite = Invite()
    session.add(new_invite)
    session.flush()
    invite_token = create_invite(invite_schema.role_id, new_invite.id)
    log = Log(
        user_id=user.id,
        action="register_invite",
        description=f"Convite para o cargo de ID {invite_schema.role_id} foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(new_invite)
    return invite_token


def get_invite_by_id_or_none(invite_id: int, session: Session) -> Invite | None:
    invite = session.execute(
        select(Invite).where(Invite.id == invite_id)
    ).scalar_one_or_none()
    return invite


def check_invitation_status(invite_id: int, session: Session):
    invite = session.execute(
        select(Invite).where(Invite.id == invite_id, Invite.used)
    ).scalar_one_or_none()
    if invite:
        raise UsedInvitation


def verify_invite(token: str, session: Session):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        invite_id = int(dict_info.get("id"))
        role_id = int(dict_info.get("role"))
    except InvalidTokenError:
        raise InvalidInvite
    role = get_position_by_id_or_none(role_id=role_id, session=session)
    if not role:
        raise PositionNotFound
    check_invitation_status(invite_id=invite_id, session=session)
    valid_invite = get_invite_by_id_or_none(invite_id=invite_id, session=session)
    valid_invite.used = True
    return role.id
