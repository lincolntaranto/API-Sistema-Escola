from models.turma import Turnos

from typing import Optional

from pydantic import BaseModel

class TurmaUpdateSchema(BaseModel):
    nome: Optional[str] = None
    serie: Optional[str] = None
    ano: Optional[int] = None
    turno: Optional[Turnos] = None

class Config:
    from_attributes = True