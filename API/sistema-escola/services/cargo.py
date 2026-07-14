from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.cargo_exceptions import PositionNotFound
from models import Usuario, Cargo, Log


def consult_position(id_cargo: int, session: Session, usuario: Usuario) -> Cargo:
    cargo = session.execute(
        select(Cargo).where(Cargo.id == id_cargo)
    ).scalar_one_or_none()
    if not cargo:
        raise PositionNotFound
    log = Log(
        id_usuario=usuario.id,
        acao="consultar_cargo",
        descricao=f"Cargo {cargo.nome}, de ID {cargo.id}, foi consultado.",
    )
    session.add(log)
    session.commit()
    return cargo
