from sqlalchemy import select
from sqlalchemy.orm import Session

from core.security import verificar_autorizacao
from exceptions.cargo_exceptions import PositionNotFound, PositionAlreadyExists
from models import Usuario, Cargo, Log
from schemas.cargo import CargoSchema


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


def register_position(
    cargo_schema: CargoSchema, session: Session, usuario: Usuario
) -> Cargo:
    verificar_autorizacao(usuario)
    cargo = session.execute(
        select(Cargo).where(Cargo.nome == cargo_schema.nome)
    ).scalar_one_or_none()
    if cargo:
        raise PositionAlreadyExists
    novo_cargo = Cargo(nome=cargo_schema.nome)
    session.add(novo_cargo)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_cargo",
        descricao=f"Cargo {novo_cargo.nome}, de ID {novo_cargo.id}, foi cadastrado!",
    )
    session.add(log)
    session.commit()
    session.refresh(novo_cargo)
    return novo_cargo
