from sqlalchemy import select
from sqlalchemy.orm import Session

from core.crud import update_model
from exceptions.aluno_exceptions import (
    StudentNotFound,
    StudentAlreadyExists,
)
from exceptions.turma_exceptions import ClassroomNotFound
from models import Aluno, Usuario, Log, Turma
from schemas.aluno.aluno import AlunoSchema
from schemas.aluno.aluno_update import AlunoUpdateSchema


def consult_student_by_id(
    id_aluno: int,
    session: Session,
    usuario: Usuario,
) -> Aluno:
    aluno = session.execute(
        select(Aluno).where(Aluno.id == id_aluno)
    ).scalar_one_or_none()

    if not aluno or aluno.deletado:
        raise StudentNotFound()

    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="consultar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi consultado.",
    )
    session.add(log)
    session.commit()
    return aluno


def register_student(
    aluno_schema: AlunoSchema, session: Session, usuario: Usuario
) -> Aluno:
    aluno = session.execute(
        select(Aluno).where(
            Aluno.nome == aluno_schema.nome,
            Aluno.data_nascimento == aluno_schema.data_nascimento,
            Aluno.nome_responsavel == aluno_schema.nome_responsavel,
        )
    ).scalar_one_or_none()
    turma = session.execute(
        select(Turma).where(Turma.id == aluno_schema.turma)
    ).scalar_one_or_none()

    if not turma:
        raise ClassroomNotFound
    if aluno:
        raise StudentAlreadyExists

    novo_aluno = Aluno(
        nome=aluno_schema.nome,
        data_nascimento=aluno_schema.data_nascimento,
        turma=aluno_schema.turma,
        nome_responsavel=aluno_schema.nome_responsavel,
        celular_responsavel=aluno_schema.celular_responsavel,
    )
    session.add(novo_aluno)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        id_aluno=novo_aluno.id,
        acao="cadastrar_aluno",
        descricao=f"Aluno {novo_aluno.nome}, da turma {novo_aluno.turma} foi cadastrado.",
    )
    session.add(log)
    session.commit()
    session.refresh(novo_aluno)
    return novo_aluno


def delete_student(id_aluno: int, session: Session, usuario: Usuario) -> Aluno:
    aluno = session.execute(
        select(Aluno).where(Aluno.id == id_aluno)
    ).scalar_one_or_none()
    if not aluno or aluno.deletado:
        raise StudentNotFound
    aluno.deletado = True
    session.add(aluno)
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="deletar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi deletado.",
    )
    session.add(log)
    session.commit()
    return aluno


def update_student(
    id_aluno: int,
    aluno_update_schema: AlunoUpdateSchema,
    session: Session,
    usuario: Usuario,
) -> Aluno:
    aluno = session.get(Aluno, id_aluno)
    if not aluno or aluno.deletado:
        raise StudentNotFound
    update_model(obj=aluno, schema=aluno_update_schema)
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="atualizar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi atualizado.",
    )

    session.add(log)
    session.commit()
    session.refresh(aluno)
    return aluno
