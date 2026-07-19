from pydantic import BaseModel


class GradeSchema(BaseModel):
    student_id: int
    school_subject: str
    grade: float
    bimester: int
    year: int
