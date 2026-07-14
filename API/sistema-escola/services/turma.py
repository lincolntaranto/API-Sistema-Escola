from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.turma_exceptions import ClassroomNotFound, ClassroomAlreadyExists
from models import Turma, Usuario, Log
from schemas.turma.turma import TurmaSchema


def consult_classroom(id_turma: int, session: Session, usuario: Usuario) -> Turma:
    turma = session.execute(
        select(Turma).where(Turma.id == id_turma)
    ).scalar_one_or_none()
    if not turma:
        raise ClassroomNotFound
    log = Log(
        id_usuario=usuario.id,
        # id_turma=turma.id, // adição futura
        acao="consultar_turma",
        descricao=f"Turma {turma.nome}, de ID {turma.id}, foi consultada.",
    )
    session.add(log)
    session.commit()
    return turma


def register_classroom(turma_schema: TurmaSchema, session: Session, usuario: Usuario):
    turma = session.execute(
        select(Turma).where(
            Turma.nome == turma_schema.nome,
            Turma.serie == turma_schema.serie,
            Turma.turno == turma_schema.turno,
        )
    ).scalar_one_or_none()
    if turma:
        raise ClassroomAlreadyExists
    nova_turma = Turma(
        nome=turma_schema.nome,
        serie=turma_schema.serie,
        ano=turma_schema.ano,
        turno=turma_schema.turno,
    )
    session.add(nova_turma)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        acao="cadastrar_turma",
        descricao=f"Turma {nova_turma.nome}, de ID {nova_turma.id}, foi cadastrada!",
    )
    session.add(log)
    session.commit()
    session.refresh(nova_turma)
    return nova_turma


def delete_classroom(id_turma: int, session: Session, usuario: Usuario) -> Turma:
    turma = session.execute(
        select(Turma).where(Turma.id == id_turma)
    ).scalar_one_or_none()
    if not turma:
        raise ClassroomNotFound
    session.delete(turma)
    log = Log(
        id_usuario=usuario.id,
        acao="deletar_turma",
        descricao=f"Turma {turma.nome}, de id {turma.id} foi deletada.",
    )
    session.add(log)
    session.commit()
    return turma
