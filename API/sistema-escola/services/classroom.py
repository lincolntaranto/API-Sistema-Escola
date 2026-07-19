from sqlalchemy import select
from sqlalchemy.orm import Session

from core.crud import update_model
from exceptions.classroom_exceptions import ClassroomNotFound, ClassroomAlreadyExists
from models import Classroom, User, Log
from schemas.classroom.classroom import ClassroomSchema
from schemas.classroom.classroom_update import ClassroomUpdateSchema


def consult_classroom(classroom_id: int, session: Session, user: User) -> Classroom:
    classroom = session.execute(
        select(Classroom).where(Classroom.id == classroom_id)
    ).scalar_one_or_none()
    if not classroom:
        raise ClassroomNotFound
    log = Log(
        user_id=user.id,
        # classroom_id=classroom.id, // adição futura
        action="consult_classroom",
        description=f"Turma {classroom.name}, de ID {classroom.id}, foi consultada.",
    )
    session.add(log)
    session.commit()
    return classroom


def register_classroom(classroom_schema: ClassroomSchema, session: Session, user: User):
    classroom = session.execute(
        select(Classroom).where(
            Classroom.name == classroom_schema.name,
            Classroom.school_year == classroom_schema.school_year,
            Classroom.shift == classroom_schema.shift,
        )
    ).scalar_one_or_none()
    if classroom:
        raise ClassroomAlreadyExists
    new_classroom = Classroom(
        name=classroom_schema.name,
        school_year=classroom_schema.school_year,
        year=classroom_schema.year,
        shift=classroom_schema.shift,
    )
    session.add(new_classroom)
    session.flush()
    log = Log(
        user_id=user.id,
        action="register_classroom",
        description=f"Turma {new_classroom.name}, de ID {new_classroom.id}, foi cadastrada!",
    )
    session.add(log)
    session.commit()
    session.refresh(new_classroom)
    return new_classroom


def delete_classroom(classroom_id: int, session: Session, user: User) -> Classroom:
    classroom = session.execute(
        select(Classroom).where(Classroom.id == classroom_id)
    ).scalar_one_or_none()
    if not classroom:
        raise ClassroomNotFound
    session.delete(classroom)
    log = Log(
        user_id=user.id,
        action="delete_classroom",
        description=f"Turma {classroom.name}, de id {classroom.id} foi deletada.",
    )
    session.add(log)
    session.commit()
    return classroom


def update_classroom(
    classroom_id: int,
    classroom_update_schema: ClassroomUpdateSchema,
    session: Session,
    user: User,
) -> Classroom:
    classroom = session.execute(
        select(Classroom).where(Classroom.id == classroom_id)
    ).scalar_one_or_none()

    if not classroom:
        raise ClassroomNotFound

    update_model(obj=classroom, schema=classroom_update_schema)
    log = Log(
        user_id=user.id,
        action="update_classroom",
        description=f"Turma {classroom.name}, de ID {classroom.id}, foi atualizada.",
    )

    session.add(log)
    session.commit()
    session.refresh(classroom)

    return classroom
