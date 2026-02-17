from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.core.auth_dependency import get_current_user

from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.marks import Marks

from app.schemas.analytics_schema import (
    DepartmentLeaderboardResponse,
    YearPerformanceResponse,
    CourseTopperResponse,
    DashboardAnalyticsResponse
)

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


# ------------------- Helper function to calculate GPA -------------------
def calculate_student_gpa(db: Session, student_id: int):
    marks = db.query(Marks).filter(Marks.student_id == student_id).all()

    if not marks:
        return None

    total_gp = sum(m.grade_points for m in marks)
    return total_gp / len(marks)


# ------------------- 1) Department Leaderboard -------------------
@router.get("/department-leaderboard", response_model=list[DepartmentLeaderboardResponse])
def department_leaderboard(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    departments = db.query(Student.department).distinct().all()
    results = []

    for dept_tuple in departments:
        dept = dept_tuple[0]

        students = db.query(Student).filter(Student.department == dept).all()

        gpas = []
        topper_name = None
        topper_gpa = None

        for student in students:
            gpa = calculate_student_gpa(db, student.id)

            if gpa is not None:
                gpas.append(gpa)

                if topper_gpa is None or gpa > topper_gpa:
                    topper_gpa = gpa
                    topper_name = student.name

        avg_gpa = sum(gpas) / len(gpas) if gpas else 0

        results.append(
            DepartmentLeaderboardResponse(
                department=dept,
                total_students=len(students),
                avg_gpa=round(avg_gpa, 2),
                topper_name=topper_name,
                topper_gpa=round(topper_gpa, 2) if topper_gpa else None
            )
        )

    results.sort(key=lambda x: x.avg_gpa, reverse=True)
    return results


# ------------------- 2) Year-wise Performance -------------------
@router.get("/year-performance", response_model=list[YearPerformanceResponse])
def year_performance(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    years = db.query(Student.year).distinct().all()
    output = []

    for year_tuple in years:
        year = year_tuple[0]

        students = db.query(Student).filter(Student.year == year).all()

        gpas = []
        attendance_percentages = []

        for student in students:
            gpa = calculate_student_gpa(db, student.id)
            if gpa is not None:
                gpas.append(gpa)

            total_classes = db.query(Attendance).filter(
                Attendance.student_id == student.id
            ).count()

            present_classes = db.query(Attendance).filter(
                Attendance.student_id == student.id,
                Attendance.status == "present"
            ).count()

            if total_classes > 0:
                attendance_percentages.append((present_classes / total_classes) * 100)

        avg_gpa = sum(gpas) / len(gpas) if gpas else 0
        avg_attendance = sum(attendance_percentages) / len(attendance_percentages) if attendance_percentages else 0

        output.append(
            YearPerformanceResponse(
                year=year,
                total_students=len(students),
                avg_gpa=round(avg_gpa, 2),
                avg_attendance_percentage=round(avg_attendance, 2)
            )
        )

    output.sort(key=lambda x: x.year)
    return output


# ------------------- 3) Course Toppers (All Courses) -------------------
@router.get("/course-toppers", response_model=list[CourseTopperResponse])
def course_toppers(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    courses = db.query(Course).all()
    result = []

    for course in courses:
        topper_mark = db.query(Marks).filter(Marks.course_id == course.id).order_by(Marks.grade_points.desc()).first()

        if not topper_mark:
            continue

        topper_student = db.query(Student).filter(Student.id == topper_mark.student_id).first()

        if not topper_student:
            continue

        result.append(
            CourseTopperResponse(
                course_id=course.id,
                course_code=course.course_code,
                course_name=course.course_name,
                topper_student_name=topper_student.name,
                topper_roll_no=topper_student.roll_no,
                grade=topper_mark.grade,
                grade_points=topper_mark.grade_points
            )
        )

    return result


# ------------------- 4) Dashboard Analytics -------------------
@router.get("/dashboard", response_model=DashboardAnalyticsResponse)
def dashboard_analytics(db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    total_students = db.query(Student).count()
    total_courses = db.query(Course).count()
    total_enrollments = db.query(Enrollment).count()
    total_attendance_records = db.query(Attendance).count()
    total_marks_records = db.query(Marks).count()

    # GPA calculation
    all_marks = db.query(Marks).all()
    avg_gpa = 0

    if all_marks:
        avg_gpa = sum(m.grade_points for m in all_marks) / len(all_marks)

    # Attendance calculation
    avg_attendance = 0
    if total_attendance_records > 0:
        present_count = db.query(Attendance).filter(Attendance.status == "present").count()
        avg_attendance = (present_count / total_attendance_records) * 100

    # Defaulters (<75%)
    defaulters = 0
    students = db.query(Student).all()

    for student in students:
        total_classes = db.query(Attendance).filter(Attendance.student_id == student.id).count()

        if total_classes == 0:
            continue

        present_classes = db.query(Attendance).filter(
            Attendance.student_id == student.id,
            Attendance.status == "present"
        ).count()

        percentage = (present_classes / total_classes) * 100

        if percentage < 75:
            defaulters += 1

    return DashboardAnalyticsResponse(
        total_students=total_students,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_attendance_records=total_attendance_records,
        total_marks_records=total_marks_records,
        avg_gpa=round(avg_gpa, 2),
        avg_attendance_percentage=round(avg_attendance, 2),
        total_defaulters=defaulters
    )
