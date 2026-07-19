from pydantic import BaseModel, ConfigDict


class InviteSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    role_id: int
