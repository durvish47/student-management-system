from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.student import Student
from app.models.attendance import Attendance
from app.schemas.defaulters_schema import DefaulterStudentResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/defaulters", response_model=list[DefaulterStudentResponse])
def get_attendance_defaulters(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    threshold: float = Query(75, ge=0, le=100),
    department: str = Query(None),
    year: int = Query(None)
):
    query = db.query(Student)

    if department:
        query = query.filter(Student.department == department)

    if year:
        query = query.filter(Student.year == year)

    students = query.all()
    defaulters = []

    for student in students:
        total_classes = db.query(Attendance).filter(
            Attendance.student_id == student.id
        ).count()

        if total_classes == 0:
            continue

        attended_classes = db.query(Attendance).filter(
            Attendance.student_id == student.id,
            Attendance.status == "present"
        ).count()

        percentage = (attended_classes / total_classes) * 100

        if percentage < threshold:
            defaulters.append(
                DefaulterStudentResponse(
                    student_id=student.id,
                    student_name=student.name,
                    roll_no=student.roll_no,
                    department=student.department,
                    year=student.year,
                    attendance_percentage=round(percentage, 2)
                )
            )

    defaulters.sort(key=lambda x: x.attendance_percentage)

    return defaulters
