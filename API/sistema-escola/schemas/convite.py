from pydantic import BaseModel


class ConviteSchema(BaseModel):
    id_cargo: int

    class Config:
        from_attributes = True
