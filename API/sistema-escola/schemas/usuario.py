from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    nome: str
    senha: str
    cargo: int
    email: str
    numero: str

    class Config:
        from_attributes = True
