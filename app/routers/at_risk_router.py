from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.schemas.at_risk_schema import AtRiskStudentResponse

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/at-risk", response_model=list[AtRiskStudentResponse])
def get_students_at_risk(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    attendance_threshold: float = Query(75, ge=0, le=100),
    gpa_threshold: float = Query(6.0, ge=0, le=10),
):
    students = db.query(Student).all()
    at_risk_list = []

    for student in students:
        # Attendance Calculation
        total_classes = db.query(Attendance).filter(
            Attendance.student_id == student.id
        ).count()

        present_classes = db.query(Attendance).filter(
            Attendance.student_id == student.id,
            Attendance.status == "present"
        ).count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = (present_classes / total_classes) * 100

        # GPA Calculation
        marks = db.query(Marks).filter(Marks.student_id == student.id).all()

        gpa = 0
        if marks:
            total_gp = sum(m.grade_points for m in marks)
            gpa = total_gp / len(marks)

        # Risk Conditions
        risk_reasons = []

        if attendance_percentage < attendance_threshold:
            risk_reasons.append("Low Attendance")

        if gpa < gpa_threshold:
            risk_reasons.append("Low GPA")

        if risk_reasons:
            at_risk_list.append(
                AtRiskStudentResponse(
                    student_id=student.id,
                    student_name=student.name,
                    roll_no=student.roll_no,
                    department=student.department,
                    year=student.year,
                    attendance_percentage=round(attendance_percentage, 2),
                    gpa=round(gpa, 2),
                    risk_reason=" & ".join(risk_reasons)
                )
            )

    return at_risk_list
