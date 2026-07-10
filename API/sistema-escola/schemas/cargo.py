from pydantic import BaseModel


class CargoSchema(BaseModel):
    nome: str
