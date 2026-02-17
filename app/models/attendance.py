from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, Date
from datetime import date
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    attendance_date = Column(Date, default=date.today, nullable=False)

    status = Column(String(20), nullable=False) 

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", "attendance_date", name="unique_attendance_record"),
    )