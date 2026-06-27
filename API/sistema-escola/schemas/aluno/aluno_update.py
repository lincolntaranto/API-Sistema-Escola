from datetime import date
from typing import Optional

from pydantic import BaseModel


class AlunoUpdateSchema(BaseModel):
    nome: Optional[str] = None
    data_nascimento: Optional[date] = None
    turma: Optional[int] = None
    nome_responsavel: Optional[str] = None
    celular_responsavel: Optional[str] = None

    class Config:
        from_attributes = True
