from pydantic import BaseModel


class NotaSchema(BaseModel):
    id_aluno: int
    materia: str
    nota: float
    bimestre: int
    ano: int
