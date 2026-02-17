from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.schemas.report_schema import StudentReportResponse, CourseReport

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/student/{student_id}", response_model=StudentReportResponse)
def get_student_report(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # FIXED: must be .all() not .first()
    enrollments = db.query(Enrollment).filter(
        Enrollment.student_id == student_id
    ).all()

    course_reports = []
    total_grade_points = 0
    grade_count = 0

    for enrollment in enrollments:

        course = db.query(Course).filter(
            Course.id == enrollment.course_id
        ).first()

        if not course:
            continue

        # Total classes marked for this student in this course
        total_classes = db.query(Attendance).filter(
            Attendance.course_id == course.id,
            Attendance.student_id == student_id
        ).count()

        # FIXED: Present should match exactly what you store in DB
        attended_classes = db.query(Attendance).filter(
            Attendance.course_id == course.id,
            Attendance.student_id == student_id,
            Attendance.status == "Present"
        ).count()

        attendance_percentage = 0
        if total_classes > 0:
            attendance_percentage = (attended_classes / total_classes) * 100

        marks = db.query(Marks).filter(
            Marks.student_id == student_id,
            Marks.course_id == course.id
        ).first()

        marks_obtained = None
        total_marks = None
        percentage = None
        grade = None
        grade_points = None

        if marks:
            marks_obtained = marks.marks_obtained
            total_marks = marks.total_marks
            percentage = marks.percentage
            grade = marks.grade
            grade_points = marks.grade_points

            # FIXED: add grade points to total
            total_grade_points += grade_points
            grade_count += 1

        course_reports.append(
            CourseReport(
                course_id=course.id,
                course_code=course.course_code,
                course_name=course.course_name,   # FIXED: missing before

                total_classes=total_classes,
                attended_classes=attended_classes,
                attendance_percentage=round(attendance_percentage, 2),

                marks_obtained=marks_obtained,
                total_marks=total_marks,
                percentage=percentage,
                grade=grade,
                grade_points=grade_points
            )
        )

    gpa = 0
    if grade_count > 0:
        gpa = total_grade_points / grade_count

    return StudentReportResponse(
        student_id=student.id,
        student_name=student.name,
        roll_no=student.roll_no,
        department=student.department,
        year=student.year,
        gpa=round(gpa, 2),
        total_courses=len(course_reports),
        courses=course_reports
    )
