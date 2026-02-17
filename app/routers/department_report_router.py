from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.marks import Marks
from app.schemas.department_report_schema import DepartmentReportResponse, DepartmentTopperResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/department/{department_name}", response_model=DepartmentReportResponse)
def get_department_report(
    department_name: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    students = db.query(Student).filter(Student.department == department_name).all()

    if not students:
        raise HTTPException(status_code=404, detail="No students found in this department")

    total_students = len(students)

    # Courses count (unique courses enrolled by department students)
    course_ids = db.query(Enrollment.course_id).join(Student).filter(
        Student.department == department_name
    ).distinct().all()

    total_courses = len(course_ids)

    # Grade distribution
    grade_distribution = {}

    # GPA calculation per student
    topper_list = []
    total_gpa_sum = 0
    gpa_count = 0

    for student in students:
        marks = db.query(Marks).filter(Marks.student_id == student.id).all()

        if not marks:
            continue

        student_total_gp = sum(m.grade_points for m in marks)
        student_gpa = student_total_gp / len(marks)

        total_gpa_sum += student_gpa
        gpa_count += 1

        topper_list.append(
            DepartmentTopperResponse(
                student_id=student.id,
                student_name=student.name,
                roll_no=student.roll_no,
                gpa=round(student_gpa, 2)
            )
        )

        for m in marks:
            grade_distribution[m.grade] = grade_distribution.get(m.grade, 0) + 1

    average_gpa = 0
    if gpa_count > 0:
        average_gpa = total_gpa_sum / gpa_count

    # Sort toppers by GPA descending and pick top 5
    topper_list.sort(key=lambda x: x.gpa, reverse=True)
    toppers = topper_list[:5]

    return DepartmentReportResponse(
        department=department_name,
        total_students=total_students,
        total_courses=total_courses,
        average_gpa=round(average_gpa, 2),
        grade_distribution=grade_distribution,
        toppers=toppers
    )
