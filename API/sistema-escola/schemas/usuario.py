from pydantic import BaseModel, EmailStr


class UsuarioSchema(BaseModel):
    nome: str
    senha: str
    convite: str
    email: EmailStr
    numero: str
