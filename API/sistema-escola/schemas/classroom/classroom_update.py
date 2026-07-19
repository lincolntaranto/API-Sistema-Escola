from models.classroom import Shifts

from typing import Optional

from pydantic import BaseModel, ConfigDict


class ClassroomUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = None
    school_year: Optional[str] = None
    year: Optional[int] = None
    shift: Optional[Shifts] = None
