from pydantic import BaseModel

from typing import Optional


class GradeUpdateSchema(BaseModel):
    student_id: Optional[int] = None
    school_subject: Optional[str] = None
    grade: Optional[float] = None
    bimester: Optional[int] = None
    year: Optional[int] = None
