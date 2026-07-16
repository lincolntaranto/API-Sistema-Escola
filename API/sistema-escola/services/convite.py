from sqlalchemy import select
from sqlalchemy.orm import Session

from core.authorization import verificar_autorizacao, criar_convite
from exceptions.cargo_exceptions import PositionNotFound
from models import Usuario, Convite, Cargo, Log
from schemas.convite import ConviteSchema


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
