from sqlalchemy import Column, Integer, ForeignKey, Date, UniqueConstraint
from datetime import date
from app.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_date = Column(Date, default=date.today)

    __table_args__ = (UniqueConstraint("student_id", "course_id", name="unique_student_course"),)