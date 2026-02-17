from pydantic import BaseModel
from typing import Optional

class CourseReport(BaseModel):
    course_id: int
    course_code: str
    course_name: str

    total_classes: int
    attended_classes: int
    attendance_percentage: float

    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    percentage: Optional[float] = None
    grade: Optional[str] = None
    grade_points: Optional[float] = None

class StudentReportResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    department: str
    year: int

    gpa: float
    total_courses: int

    courses: list[CourseReport]
