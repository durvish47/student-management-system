from pydantic import BaseModel


class AtRiskStudentResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    department: str
    year: int

    attendance_percentage: float
    gpa: float

    risk_reason: str

    class Config:
        from_attributes = True
