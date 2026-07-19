from sqlalchemy import select, func
from sqlalchemy.orm import Session

from core.crud import update_model
from exceptions.student_exceptions import (
    StudentNotFound,
    StudentAlreadyExists,
)
from exceptions.classroom_exceptions import ClassroomNotFound
from models import Student, User, Log, Classroom
from schemas.student.student import StudentSchema
from schemas.student.student_update import StudentUpdateSchema


def consult_student_by_id(
    student_id: int,
    session: Session,
    user: User,
) -> Student:
    student = session.execute(
        select(Student).where(Student.id == student_id)
    ).scalar_one_or_none()

    if not student or student.deleted:
        raise StudentNotFound()

    log = Log(
        user_id=user.id,
        student_id=student.id,
        action="consult_student",
        description=f"Aluno {student.name}, da turma {student.classroom} foi consultado.",
    )
    session.add(log)
    session.commit()
    return student


def register_student(
    student_schema: StudentSchema, session: Session, user: User
) -> Student:
    student = session.execute(
        select(Student).where(
            Student.name == student_schema.name,
            Student.birth_date == student_schema.birth_date,
            Student.parents_name == student_schema.guardian_name,
        )
    ).scalar_one_or_none()
    classroom = session.execute(
        select(Classroom).where(Classroom.id == student_schema.classroom)
    ).scalar_one_or_none()

    if not classroom:
        raise ClassroomNotFound
    if student:
        raise StudentAlreadyExists

    new_student = Student(
        name=student_schema.name,
        birth_date=student_schema.birth_date,
        classroom=student_schema.classroom,
        parents_name=student_schema.guardian_name,
        guardian_phone=student_schema.guardian_phone,
    )
    session.add(new_student)
    session.flush()
    log = Log(
        user_id=user.id,
        student_id=new_student.id,
        action="register_student",
        description=f"Aluno {new_student.name}, da turma {new_student.classroom} foi cadastrado.",
    )
    session.add(log)
    session.commit()
    session.refresh(new_student)
    return new_student


def delete_student(student_id: int, session: Session, user: User) -> Student:
    student = session.execute(
        select(Student).where(Student.id == student_id)
    ).scalar_one_or_none()
    if not student or student.deleted:
        raise StudentNotFound
    student.deleted = True
    session.add(student)
    log = Log(
        user_id=user.id,
        student_id=student.id,
        action="delete_student",
        description=f"Aluno {student.name}, da turma {student.classroom} foi deletado.",
    )
    session.add(log)
    session.commit()
    return student


def update_student(
    student_id: int,
    student_update_schema: StudentUpdateSchema,
    session: Session,
    user: User,
) -> Student:
    student = session.get(Student, student_id)
    if not student or student.deleted:
        raise StudentNotFound
    update_model(obj=student, schema=student_update_schema)
    log = Log(
        user_id=user.id,
        student_id=student.id,
        action="update_student",
        description=f"Aluno {student.name}, da turma {student.classroom} foi atualizado.",
    )

    session.add(log)
    session.commit()
    session.refresh(student)
    return student


def list_students(
    session: Session,
    classroom: int | None = None,
    name: str | None = None,
    page: int = 1,
    size: int = 20,
) -> tuple[list[Student], int]:
    query = select(Student).where(Student.deleted.is_(False))

    if classroom is not None:
        query = query.where(Student.classroom == classroom)
    if name is not None:
        query = query.where(Student.name.ilike(f"%{name}%"))

    total = (
        session.execute(select(func.count()).select_from(query.subquery())).scalar()
        or 0
    )

    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

    students = list(session.execute(query).scalars().all())
    return students, total
