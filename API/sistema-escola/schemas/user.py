from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    name: str
    password: str
    invite: str
    email: EmailStr
    phone: str
