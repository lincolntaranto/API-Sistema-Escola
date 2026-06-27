from pydantic import BaseModel


class NotaSchema(BaseModel):
    aluno: int
    materia: str
    nota: float
    bimestre: int
    ano: int

    class Config:
        from_attributes = True
