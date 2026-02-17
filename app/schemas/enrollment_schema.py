from pydantic import BaseModel
from datetime import date

class EnrollmentCreate(BaseModel):
    student_id: int
    course_id: int

class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    enrolled_date: date

    class Config:
        from_attributes = True