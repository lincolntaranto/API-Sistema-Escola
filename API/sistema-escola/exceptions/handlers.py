from fastapi import FastAPI
from starlette.responses import JSONResponse

from exceptions.aluno_exceptions import AlunoNaoEncontrado


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(AlunoNaoEncontrado)
    async def _(request, exc):
        return JSONResponse(
            status_code=404, content={"detail": "ID de aluno inexistente!"}
        )
