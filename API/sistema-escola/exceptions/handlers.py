from fastapi import FastAPI
from starlette.responses import JSONResponse

from exceptions.aluno_exceptions import (
    StudentNotFound,
    ClassroomNotFound,
    StudentAlreadyExists,
)


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(StudentNotFound)
    async def _(request, exc):
        return JSONResponse(
            status_code=404, content={"detail": "ID de aluno inexistente!"}
        )

    @app.exception_handler(ClassroomNotFound)
    async def _(request, exc):
        return JSONResponse(status_code=404, content={"detail": "Turma inexistente!"})

    @app.exception_handler(StudentAlreadyExists)
    async def _(request, exc):
        return JSONResponse(status_code=400, content="Aluno já cadastrado!")
