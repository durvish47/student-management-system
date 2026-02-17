from pydantic import BaseModel
from typing import List, Dict, Optional


class TopperResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    marks_obtained: float
    percentage: float
    grade: str
    grade_points: float


class CourseReportResponse(BaseModel):
    course_id: int
    course_code: str
    course_name: str
    credits: int

    total_enrolled: int

    average_marks: Optional[float] = None
    highest_marks: Optional[float] = None
    lowest_marks: Optional[float] = None

    average_attendance_percentage: float

    grade_distribution: Dict[str, int]

    toppers: List[TopperResponse]
