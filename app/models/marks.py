from sqlalchemy import Column, Integer, Float, String, ForeignKey, UniqueConstraint
from app.database import Base

class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

    marks_obtained = Column(Float, nullable=False)
    total_marks = Column(Float, nullable=False)

    percentage = Column(Float, nullable=False)

    grade = Column(String(5), nullable=False)
    grade_points = Column(Float, nullable=False)

    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="unique_student_course_mark"),
    )