from pydantic import BaseModel
from datetime import date
from typing import Optional

class AttendanceCreate(BaseModel):
    student_id: int
    course_id: int
    attendance_date: Optional[date] = None
    status: str

class AttendanceUpdate(BaseModel):
    status: str

class AttendanceResponse(BaseModel):
    id: int
    student_id: int
    course_id: int
    attendance_date: date
    status: str

    class Config:
        from_attributes = True