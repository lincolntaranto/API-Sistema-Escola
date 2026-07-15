from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.nota_exceptions import GradeNotFound
from models import Usuario, Nota, Log
from services.aluno import consult_student_by_id


def consult_grade(
    id_aluno: int,
    materia: str,
    bimestre: int,
    ano: int,
    session: Session,
    usuario: Usuario,
) -> Nota:
    aluno = consult_student_by_id(id_aluno=id_aluno, session=session, usuario=usuario)
    nota = session.execute(
        select(Nota).where(
            Nota.id_aluno == id_aluno,
            Nota.materia == materia,
            Nota.bimestre == bimestre,
            Nota.ano == ano,
        )
    ).scalar_one_or_none()
    if not nota:
        raise GradeNotFound
    log = Log(
        id_usuario=usuario.id,
        id_aluno=aluno.id,
        acao="consultar_nota",
        descricao=f"Aluno {aluno.nome}, da turma {aluno.turma} teve a nota consultada.",
    )
    session.add(log)
    session.commit()
    return nota
