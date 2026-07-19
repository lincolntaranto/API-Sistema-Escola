from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models.session import get_session
from models import User
from schemas.student.student import StudentSchema
from schemas.student.student_update import StudentUpdateSchema
from schemas.role import RoleSchema
from schemas.invite import InviteSchema
from schemas.grade.grade import GradeSchema
from schemas.grade.grade_update import GradeUpdateSchema
from schemas.classroom.classroom import ClassroomSchema
from schemas.classroom.classroom_update import ClassroomUpdateSchema
from services.auth import verify_token
from core.authorization import verify_authorization
from services.student import (
    consult_student_by_id,
    register_student,
    delete_student,
    update_student,
    list_students,
)
from services.role import (
    consult_role,
    register_role,
    delete_role,
    update_role,
)
from services.invite import register_invite
from services.grade import consult_grade, register_grade, update_grade
from services.classroom import (
    consult_classroom,
    register_classroom,
    delete_classroom,
    update_classroom,
)

management_router = APIRouter(tags=["management"])


@management_router.get("/students/{student_id}")
async def get_student(
    student_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para consultar alunos registrados no sistema."""

    student = consult_student_by_id(student_id=student_id, session=session, user=user)
    return {
        "name": student.name,
        "classroom": student.classroom,
        "birth_date": student.birth_date,
        "guardian_name": student.parents_name,
        "guardian_phone": student.guardian_phone,
    }


@management_router.get("/students")
async def get_students(
    classroom: int | None = None,
    name: str | None = None,
    page: int = 1,
    size: int = 20,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para listar alunos com filtros e paginação."""
    students, total = list_students(
        session=session,
        classroom=classroom,
        name=name,
        page=page,
        size=size,
    )
    return {
        "items": [
            {
                "id": student.id,
                "name": student.name,
                "classroom": student.classroom,
                "birth_date": student.birth_date,
            }
            for student in students
        ],
        "page": page,
        "size": size,
        "total": total,
        "total_pages": (total + size - 1) // size,
    }


@management_router.post("/students")
async def create_student(
    student_schema: StudentSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para cadastrar um aluno no sistema"""

    new_student = register_student(
        student_schema=student_schema, session=session, user=user
    )
    return {
        "mensagem": "Aluno cadastrado com sucesso!",
        "id": new_student.id,
        "name": new_student.name,
        "classroom": new_student.classroom,
    }


@management_router.delete("/students/{student_id}")
async def remove_student(
    student_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para deletar um aluno do sistema"""

    student = delete_student(student_id=student_id, session=session, user=user)
    return {
        "mensagem": "Aluno deletado com sucesso!",
        "id": student.id,
        "name": student.name,
        "classroom": student.classroom,
    }


@management_router.patch("/students/{student_id}")
async def patch_student(
    student_id: int,
    student_update_schema: StudentUpdateSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para atualizar um aluno do sistema."""

    student = update_student(
        student_id=student_id,
        student_update_schema=student_update_schema,
        session=session,
        user=user,
    )

    return {
        "mensagem": "Aluno atualizado com sucesso!",
        "id": student.id,
        "name": student.name,
    }


@management_router.get("/classrooms/{classroom_id}")
async def get_classroom(
    classroom_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para consultar turmas no sistema"""

    classroom = consult_classroom(classroom_id=classroom_id, session=session, user=user)
    return {
        "classroom": classroom.name,
        "school_year": classroom.school_year,
        "year": classroom.year,
        "shift": classroom.shift,
    }


@management_router.post("/classrooms")
async def create_classroom(
    classroom_schema: ClassroomSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para cadastrar uma turma no sistema"""

    new_classroom = register_classroom(
        classroom_schema=classroom_schema, session=session, user=user
    )
    return {
        "mensagem": "Turma cadastrada com sucesso!",
        "id": new_classroom.id,
        "name": new_classroom.name,
        "school_year": new_classroom.school_year,
        "year": new_classroom.year,
        "shift": new_classroom.shift,
    }


@management_router.delete("/classrooms/{classroom_id}")
async def remove_classroom(
    classroom_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para apagar uma turma do sistema."""

    classroom = delete_classroom(classroom_id=classroom_id, session=session, user=user)
    return {
        "mensagem": "Turma deletada com sucesso!",
        "id": classroom.id,
        "name": classroom.name,
        "school_year": classroom.school_year,
        "shift": classroom.shift,
        "year": classroom.year,
    }


@management_router.patch("/classrooms/{classroom_id}")
async def patch_classroom(
    classroom_id: int,
    classroom_update_schema: ClassroomUpdateSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para atualizar uma turma do sistema."""

    classroom = update_classroom(
        classroom_id=classroom_id,
        classroom_update_schema=classroom_update_schema,
        session=session,
        user=user,
    )

    return {
        "mensagem": "Turma atualizada com sucesso!",
        "id": classroom.id,
        "name": classroom.name,
        "school_year": classroom.school_year,
        "year": classroom.year,
        "shift": classroom.shift,
    }


@management_router.get("/roles/{role_id}")
async def get_role(
    role_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para consultar cargos no sistema."""

    role = consult_role(role_id=role_id, session=session, user=user)
    return {"name": role.name}


@management_router.post("/roles")
async def create_role(
    role_schema: RoleSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para cadastrar um cargo no sistema."""

    verify_authorization(user)
    new_role = register_role(role_schema=role_schema, session=session, user=user)
    return {
        "mensagem": "Cargo cadastrado com sucesso!",
        "id": new_role.id,
        "name": new_role.name,
    }


@management_router.delete("/roles/{role_id}")
async def remove_role(
    role_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para apagar um cargo do sistema."""

    verify_authorization(user)
    role = delete_role(role_id=role_id, session=session, user=user)
    return {
        "mensagem": "Cargo deletado com sucesso!",
        "id": role.id,
        "name": role.name,
    }


@management_router.patch("/roles/{role_id}")
async def patch_role(
    role_id: int,
    role_schema: RoleSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para atualizar um cargo no sistema."""

    verify_authorization(user)
    role = update_role(
        role_id=role_id, role_schema=role_schema, session=session, user=user
    )

    return {"mensagem": "Cargo atualizado com sucesso!", "id": role.id}


@management_router.get("/students/{student_id}/grades")
async def get_grades(
    student_id: int,
    school_subject: str,
    bimester: int,
    year: int,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """ "Rota para consultar notas de alunos no sistema."""
    grade = consult_grade(
        student_id=student_id,
        school_subject=school_subject,
        bimester=bimester,
        year=year,
        session=session,
        user=user,
    )
    return {
        "name": grade.student_id,
        "year": grade.year,
        "school_subject": grade.school_subject,
        "bimester": grade.bimester,
        "grade": grade.grade,
    }


@management_router.post("/grades")
async def create_grade(
    grade_schema: GradeSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para cadastrar nota de um aluno no sistema."""

    new_grade = register_grade(grade_schema=grade_schema, session=session, user=user)
    return {
        "mensagem": "Nota cadastrada com sucesso!",
        "id": new_grade.id,
        "student_id": new_grade.student_id,
        "year": new_grade.year,
        "school_subject": new_grade.school_subject,
        "bimester": new_grade.bimester,
        "grade": new_grade.grade,
    }


@management_router.patch("/grades/{grade_id}")
async def patch_grade(
    grade_id: int,
    grade_update_schema: GradeUpdateSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para atualizar uma nota do sistema."""
    grade = update_grade(
        grade_id=grade_id,
        grade_update_schema=grade_update_schema,
        session=session,
        user=user,
    )

    return {
        "mensagem": "Nota atualizada com sucesso!",
        "id": grade.id,
        "student_id": grade.student_id,
        "year": grade.year,
        "school_subject": grade.school_subject,
        "bimester": grade.bimester,
        "grade": grade.grade,
    }


@management_router.post("/invites")
async def create_invite_route(
    invite_schema: InviteSchema,
    session: Session = Depends(get_session),
    user: User = Depends(verify_token),
):
    """Rota para cadastrar um convite no sistema."""

    verify_authorization(user)
    invite_token = register_invite(
        invite_schema=invite_schema, session=session, user=user
    )
    return {
        "mensagem": "Convite criado com sucesso!",
        "invite_token": invite_token,
        "role_id": invite_schema.role_id,
    }
