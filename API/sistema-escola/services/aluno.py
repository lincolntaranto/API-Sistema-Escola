from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.aluno_exceptions import AlunoNaoEncontrado
from models import Aluno, Usuario, Log


def consult_student_by_id(
    id_aluno: int,
    session: Session,
    usuario: Usuario,
) -> Aluno:
    aluno = session.execute(
        select(Aluno).where(Aluno.id == id_aluno)
    ).scalar_one_or_none()
    if not aluno or aluno.deletado:
        raise AlunoNaoEncontrado()
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="consultar_aluno",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} foi consultado.",
    )
    session.add(log)
    session.commit()
    return aluno
