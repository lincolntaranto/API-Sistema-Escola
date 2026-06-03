from pydantic import BaseModel

class NotaSchema(BaseModel):
    aluno: int
    materia: str
    nota: float
    bimestre: int

    class Config:
        from_attributes = True
