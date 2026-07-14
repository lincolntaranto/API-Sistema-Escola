from fastapi import FastAPI
from starlette.responses import JSONResponse

from exceptions.aluno_exceptions import (
    StudentNotFound,
    StudentAlreadyExists,
)
from exceptions.turma_exceptions import ClassroomNotFound, ClassroomAlreadyExists


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
        return JSONResponse(status_code=400, content={"detail": "Aluno já cadastrado!"})

    @app.exception_handler(ClassroomAlreadyExists)
    async def _(request, exc):
        return JSONResponse(status_code=400, content={"detail": "Turma já cadastrada!"})
