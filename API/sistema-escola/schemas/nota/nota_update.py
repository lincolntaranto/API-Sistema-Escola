from pydantic import BaseModel

from typing import Optional


class NotaUpdateSchema(BaseModel):
    aluno: Optional[int]
    materia: Optional[str]
    nota: Optional[float]
    bimestre: Optional[int]
    ano: Optional[int]

    class Config:
        from_attributes = True