from models.turma import Turnos

from pydantic import BaseModel


class TurmaSchema(BaseModel):
    nome: str
    serie: str
    ano: int
    turno: Turnos
