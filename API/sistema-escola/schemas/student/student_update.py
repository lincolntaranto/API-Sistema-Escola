from datetime import date
from typing import Optional

from pydantic import BaseModel


class StudentUpdateSchema(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    classroom: Optional[int] = None
    parents_name: Optional[str] = None
    guardian_phone: Optional[str] = None
