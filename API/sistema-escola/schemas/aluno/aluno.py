from datetime import date

from pydantic import BaseModel


class AlunoSchema(BaseModel):
    nome: str
    data_nascimento: date
    turma: int
    nome_responsavel: str
    celular_responsavel: str
