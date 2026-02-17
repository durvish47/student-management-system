from pydantic import BaseModel
from typing import Optional


class DepartmentLeaderboardResponse(BaseModel):
    department: str
    total_students: int
    avg_gpa: float
    topper_name: Optional[str] = None
    topper_gpa: Optional[float] = None


class YearPerformanceResponse(BaseModel):
    year: int
    total_students: int
    avg_gpa: float
    avg_attendance_percentage: float


class CourseTopperResponse(BaseModel):
    course_id: int
    course_code: str
    course_name: str
    topper_student_name: str
    topper_roll_no: str
    grade: str
    grade_points: float


class DashboardAnalyticsResponse(BaseModel):
    total_students: int
    total_courses: int
    total_enrollments: int
    total_attendance_records: int
    total_marks_records: int

    avg_gpa: float
    avg_attendance_percentage: float
    total_defaulters: int
