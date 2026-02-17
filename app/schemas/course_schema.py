from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    course_code: str
    course_name: str
    semester: str
    credits: int

class CourseUpdate(BaseModel):
    course_name: Optional[str] = None
    semester: Optional[str] = None
    credits: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    course_code: str
    course_name: str
    semester: int
    credits: int

    class Config:
        from_attributes = True