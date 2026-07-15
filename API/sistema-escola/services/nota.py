from sqlalchemy import select
from sqlalchemy.orm import Session

from exceptions.nota_exceptions import GradeNotFound, GradeAlreadyExists
from models import Usuario, Nota, Log
from schemas.nota.nota import NotaSchema
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


def register_grade(nota_schema: NotaSchema, session: Session, usuario: Usuario) -> Nota:
    nota = session.execute(
        select(Nota).where(
            Nota.id == nota_schema.id_aluno,
            Nota.materia == nota_schema.materia,
            Nota.bimestre == nota_schema.bimestre,
            Nota.ano == nota_schema.ano,
        )
    ).scalar_one_or_none()
    if nota:
        raise GradeAlreadyExists
    nova_nota = Nota(
        id_aluno=nota_schema.id_aluno,
        materia=nota_schema.materia,
        nota=nota_schema.nota,
        bimestre=nota_schema.bimestre,
        ano=nota_schema.ano,
    )
    session.add(nova_nota)
    session.flush()
    log = Log(
        id_usuario=usuario.id,
        id_aluno=nova_nota.id_aluno,
        acao="cadastrar_nota",
        descricao=f"Nota de ID {nova_nota.id} da materia {nova_nota.materia}, do bimestre {nova_nota.bimestre} e do ano"
        f" {nova_nota.ano}, foi cadastrada.",
    )
    session.add(log)
    session.commit()
    session.refresh(nova_nota)
    return nova_nota
