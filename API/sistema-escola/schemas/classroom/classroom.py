from models.classroom import Shifts

from pydantic import BaseModel


class ClassroomSchema(BaseModel):
    name: str
    school_year: str
    year: int
    shift: Shifts
