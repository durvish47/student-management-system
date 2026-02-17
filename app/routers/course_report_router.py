from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.schemas.course_report_schema import CourseReportResponse, TopperResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/course/{course_id}", response_model=CourseReportResponse)
def get_course_report(course_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id
    ).all()

    total_enrolled = len(enrollments)

    # -------------------------
    # MARKS ANALYSIS
    # -------------------------
    marks_data = db.query(Marks).filter(Marks.course_id == course_id).all()

    average_marks = None
    highest_marks = None
    lowest_marks = None

    if marks_data:
        average_marks = round(sum(m.marks_obtained for m in marks_data) / len(marks_data), 2)
        highest_marks = max(m.marks_obtained for m in marks_data)
        lowest_marks = min(m.marks_obtained for m in marks_data)

    # -------------------------
    # ATTENDANCE ANALYSIS
    # -------------------------
    attendance_data = db.query(Attendance).filter(Attendance.course_id == course_id).all()

    total_classes = len(attendance_data)
    present_classes = len([a for a in attendance_data if a.status == "Present"])

    avg_attendance_percentage = 0
    if total_classes > 0:
        avg_attendance_percentage = round((present_classes / total_classes) * 100, 2)

    # -------------------------
    # GRADE DISTRIBUTION
    # -------------------------
    grade_distribution = {}

    for m in marks_data:
        grade_distribution[m.grade] = grade_distribution.get(m.grade, 0) + 1

    # -------------------------
    # TOPPERS (Top 5)
    # -------------------------
    toppers = []

    top_marks = db.query(Marks).filter(
        Marks.course_id == course_id
    ).order_by(Marks.marks_obtained.desc()).limit(5).all()

    for m in top_marks:
        student = db.query(Student).filter(Student.id == m.student_id).first()

        if student:
            toppers.append(
                TopperResponse(
                    student_id=student.id,
                    student_name=student.name,
                    roll_no=student.roll_no,
                    marks_obtained=m.marks_obtained,
                    percentage=m.percentage,
                    grade=m.grade,
                    grade_points=m.grade_points
                )
            )

    return CourseReportResponse(
        course_id=course.id,
        course_code=course.course_code,
        course_name=course.course_name,
        credits=course.credits,
        total_enrolled=total_enrolled,
        average_marks=average_marks,
        highest_marks=highest_marks,
        lowest_marks=lowest_marks,
        average_attendance_percentage=avg_attendance_percentage,
        grade_distribution=grade_distribution,
        toppers=toppers
    )
