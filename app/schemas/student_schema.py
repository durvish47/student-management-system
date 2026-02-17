from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class StudentCreate(BaseModel):
    name: str
    roll_no:str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    department: Optional[str] = None
    year: Optional[int] = None

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    department: Optional[str] = None
    year: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    name: str
    roll_no: str
    email: Optional[str]
    phone: Optional[str]
    dob: Optional[date]
    department: Optional[str]
    year: Optional[int]

    class Config:
        from_attributes = True