from datetime import date

from pydantic import BaseModel


class StudentSchema(BaseModel):
    name: str
    birth_date: date
    classroom: int
    guardian_name: str
    guardian_phone: str
