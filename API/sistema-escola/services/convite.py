import jwt
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.authorization import verificar_autorizacao, criar_convite
from core.config import settings
from core.security import ALGORITHM
from exceptions.cargo_exceptions import PositionNotFound
from exceptions.invite_exceptions import UsedInvitation, InvalidInvite
from models import Usuario, Convite, Cargo, Log
from schemas.convite import ConviteSchema
from services.cargo import get_position_by_id_or_none


def register_invite(
    convite_schema: ConviteSchema, session: Session, usuario: Usuario
) -> Convite:
    verificar_autorizacao(usuario)
    cargo = session.execute(
        select(Cargo).where(Cargo.id == convite_schema.id_cargo)
    ).scalar_one_or_none()
    if not cargo:
        raise PositionNotFound
    novo_convite = Convite()
    session.add(novo_convite)
    session.flush()
    token_convite = criar_convite(convite_schema.id_cargo, novo_convite.id)
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_convite",
        descricao=f"Convite para o cargo de ID {convite_schema.id_cargo} foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(novo_convite)
    return token_convite


def get_invite_by_id_or_none(id_invite: int, session: Session) -> Convite | None:
    invite = session.execute(
        select(Convite).where(Convite.id == id_invite)
    ).scalar_one_or_none()
    return invite


def check_invitation_status(id_invite: int, session: Session):
    invite = session.execute(
        select(Convite).where(Convite.id == id_invite, Convite.usado)
    ).scalar_one_or_none()
    if invite:
        raise UsedInvitation


def verificar_convite(token: str, session: Session):
    try:
        dict_info = jwt.decode(token, settings.SECRET_KEY, ALGORITHM)
        id_convite = int(dict_info.get("id"))
        id_cargo = int(dict_info.get("cargo"))
    except InvalidTokenError:
        raise InvalidInvite
    cargo = get_position_by_id_or_none(id_position=id_cargo, session=session)
    if not cargo:
        raise PositionNotFound
    check_invitation_status(id_invite=id_convite, session=session)
    convite_valido = get_invite_by_id_or_none(id_invite=id_convite, session=session)
    convite_valido.usado = True
    return cargo.id
