from pydantic import BaseModel
from typing import Optional


class LeaderboardStudentResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    department: str
    year: int
    gpa: float
