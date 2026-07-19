from fastapi import FastAPI
from starlette.responses import JSONResponse

from exceptions.student_exceptions import (
    StudentNotFound,
    StudentAlreadyExists,
)
from exceptions.role_exceptions import PositionNotFound, PositionAlreadyExists
from exceptions.invite_exceptions import InvalidInvite, UsedInvitation
from exceptions.grade_exceptions import GradeNotFound, GradeAlreadyExists
from exceptions.classroom_exceptions import ClassroomNotFound, ClassroomAlreadyExists
from exceptions.user_exceptions import (
    UserNotFound,
    AccessDenied,
    InsufficientPermission,
    EmailAlreadyRegistered,
    UserNotFoundOrIncorrectPassword,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StudentNotFound)
    async def _(request, exc):
        return JSONResponse(
            status_code=404, content={"detail": "ID de aluno inexistente!"}
        )

    @app.exception_handler(ClassroomNotFound)
    async def _(request, exc):
        return JSONResponse(
            status_code=404, content={"detail": "Classroom inexistente!"}
        )

    @app.exception_handler(StudentAlreadyExists)
    async def _(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Aluno já cadastrado!"})

    @app.exception_handler(ClassroomAlreadyExists)
    async def _(request, exc):
        return JSONResponse(
            status_code=400, content={"detail": "Classroom já cadastrada!"}
        )

    @app.exception_handler(PositionNotFound)
    async def _(request, exc):
        return JSONResponse(status_code=404, content={"detail": "Role inexistente!"})

    @app.exception_handler(PositionAlreadyExists)
    async def _(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Role já cadastrado!"})

    @app.exception_handler(GradeNotFound)
    async def _(request, exc):
        return JSONResponse(status_code=404, content={"detail": "Grade inexistente!"})

    @app.exception_handler(GradeAlreadyExists)
    async def _(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Grade já cadastrada!"})

    @app.exception_handler(UserNotFound)
    async def _(request, exc):
        return JSONResponse(status_code=404, content={"detail": "Usuário inexistente!"})

    @app.exception_handler(AccessDenied)
    async def _(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Acesso negado!"})

    @app.exception_handler(InsufficientPermission)
    async def _(request, exc):
        return JSONResponse(
            status_code=403, content={"detail": "Permissão insuficiente!"}
        )

    @app.exception_handler(InvalidInvite)
    async def _(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Convite invalido!"})

    @app.exception_handler(UsedInvitation)
    async def _(request, exc):
        return JSONResponse(status_code=401, content={"detail": "Convite já usado!"})

    @app.exception_handler(EmailAlreadyRegistered)
    async def _(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Email já cadastrado!"})

    @app.exception_handler(UserNotFoundOrIncorrectPassword)
    async def _(request, exc):
        return JSONResponse(
            status_code=400,
            content={"detail": "Usuário inexistente ou senha incorreta!"},
        )
