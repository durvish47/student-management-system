from pydantic import BaseModel
from typing import Optional

class MarkCreate(BaseModel):
    student_id: int
    course_id: int
    marks_obtained: float
    total_marks: float

class MarkUpdate(BaseModel):
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None

class MarkResponse(BaseModel):
    id: int

    student_id: int
    course_id: int

    marks_obtained: float
    total_marks: float

    percentage: float
    grade: str
    grade_points: float

    class Config:
        from_attributes = True