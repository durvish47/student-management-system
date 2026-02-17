from pydantic import BaseModel
from typing import List, Dict


class DepartmentTopperResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    gpa: float


class DepartmentReportResponse(BaseModel):
    department: str

    total_students: int
    total_courses: int

    average_gpa: float

    grade_distribution: Dict[str, int]

    toppers: List[DepartmentTopperResponse]
