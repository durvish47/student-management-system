from pydantic import BaseModel

class DefaulterStudentResponse(BaseModel):
    student_id: int
    student_name: str
    roll_no: str
    department: str
    year: int
    attendance_percentage: float

    class Config:
        from_attributes = True
