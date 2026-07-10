from models.turma import Turnos

from typing import Optional

from pydantic import BaseModel, ConfigDict


class TurmaUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: Optional[str] = None
    serie: Optional[str] = None
    ano: Optional[int] = None
    turno: Optional[Turnos] = None
