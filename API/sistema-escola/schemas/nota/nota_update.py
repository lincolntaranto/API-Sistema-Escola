from pydantic import BaseModel

from typing import Optional


class NotaUpdateSchema(BaseModel):
    aluno: Optional[int] = None
    materia: Optional[str] = None
    nota: Optional[float] = None
    bimestre: Optional[int] = None
    ano: Optional[int] = None

    class Config:
        from_attributes = True
