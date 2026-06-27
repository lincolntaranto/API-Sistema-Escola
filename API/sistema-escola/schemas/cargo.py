from pydantic import BaseModel


class CargoSchema(BaseModel):
    nome: str

    class Config:
        from_attributes = True
