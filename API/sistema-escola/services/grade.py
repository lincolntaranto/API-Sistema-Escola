from sqlalchemy import select
from sqlalchemy.orm import Session

from core.crud import update_model
from exceptions.grade_exceptions import GradeNotFound, GradeAlreadyExists
from models import User, Grade, Log
from schemas.grade.grade import GradeSchema
from schemas.grade.grade_update import GradeUpdateSchema
from services.student import consult_student_by_id


def consult_grade(
    student_id: int,
    school_subject: str,
    bimester: int,
    year: int,
    session: Session,
    user: User,
) -> Grade:
    student = consult_student_by_id(student_id=student_id, session=session, user=user)
    grade = session.execute(
        select(Grade).where(
            Grade.student_id == student_id,
            Grade.school_subject == school_subject,
            Grade.bimester == bimester,
            Grade.year == year,
        )
    ).scalar_one_or_none()
    if not grade:
        raise GradeNotFound
    log = Log(
        user_id=user.id,
        student_id=student.id,
        action="consult_grade",
        description=f"Aluno {student.name}, da turma {student.classroom} teve a nota consultada.",
    )
    session.add(log)
    session.commit()
    return grade


def register_grade(grade_schema: GradeSchema, session: Session, user: User) -> Grade:
    grade = session.execute(
        select(Grade).where(
            Grade.student_id == grade_schema.student_id,
            Grade.school_subject == grade_schema.school_subject,
            Grade.bimester == grade_schema.bimester,
            Grade.year == grade_schema.year,
        )
    ).scalar_one_or_none()
    if grade:
        raise GradeAlreadyExists
    new_grade = Grade(
        student_id=grade_schema.student_id,
        school_subject=grade_schema.school_subject,
        grade=grade_schema.grade,
        bimester=grade_schema.bimester,
        year=grade_schema.year,
    )
    session.add(new_grade)
    session.flush()
    log = Log(
        user_id=user.id,
        student_id=new_grade.student_id,
        action="register_grade",
        description=f"Nota de ID {new_grade.id} da materia {new_grade.school_subject}, do bimestre {new_grade.bimester} e do ano"
        f" {new_grade.year}, foi cadastrada.",
    )
    session.add(log)
    session.commit()
    session.refresh(new_grade)
    return new_grade


def update_grade(
    grade_id: int,
    grade_update_schema: GradeUpdateSchema,
    session: Session,
    user: User,
) -> Grade:
    grade = session.execute(
        select(Grade).where(Grade.id == grade_id)
    ).scalar_one_or_none()
    if not grade:
        raise GradeNotFound
    update_model(obj=grade, schema=grade_update_schema)

    log = Log(
        user_id=user.id,
        student_id=grade.student_id,
        action="update_grade",
        description=f"Nota de ID {grade.id}, da materia {grade.school_subject} e do bimestre {grade.bimester}, foi atualizada.",
    )

    session.add(log)
    session.commit()
    session.refresh(grade)
    return grade
