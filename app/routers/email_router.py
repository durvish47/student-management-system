from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user

from app.routers.report_router import get_student_report
from app.routers.leaderboard_router import get_leaderboard
from app.routers.defaulters_router import get_attendance_defaulters

from app.utils.pdf_generator import generate_student_report_pdf
from app.utils.excel_generator import generate_leaderboard_excel, generate_defaulters_excel
from app.utils.email_sender import send_email_with_attachment
from app.routers.course_report_router import get_course_report
from app.utils.pdf_generator import generate_course_report_pdf

router = APIRouter(prefix="/api/email", tags=["Email Reports"])


@router.post("/student-report/{student_id}")
def email_student_report(
    student_id: int,
    to_email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report = get_student_report(student_id, db, current_user)
    pdf_file = generate_student_report_pdf(report.model_dump())

    send_email_with_attachment(
        to_email=to_email,
        subject=f"Student Report - ID {student_id}",
        body="Attached is the student report PDF.",
        file_bytes=pdf_file.getvalue(),
        filename=f"student_report_{student_id}.pdf"
    )

    return {"message": "Student report emailed successfully"}


@router.post("/leaderboard")
def email_leaderboard(
    to_email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    leaderboard = get_leaderboard(db=db, current_user=current_user, limit=10)
    excel_file = generate_leaderboard_excel([s.model_dump() for s in leaderboard])

    send_email_with_attachment(
        to_email=to_email,
        subject="Leaderboard Report",
        body="Attached is the leaderboard Excel file.",
        file_bytes=excel_file.getvalue(),
        filename="leaderboard.xlsx"
    )

    return {"message": "Leaderboard emailed successfully"}


@router.post("/defaulters")
def email_defaulters(
    to_email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    defaulters = get_attendance_defaulters(db=db, current_user=current_user)
    excel_file = generate_defaulters_excel([d.model_dump() for d in defaulters])

    send_email_with_attachment(
        to_email=to_email,
        subject="Attendance Defaulters Report",
        body="Attached is the attendance defaulters list.",
        file_bytes=excel_file.getvalue(),
        filename="defaulters.xlsx"
    )

    return {"message": "Defaulters report emailed successfully"}
@router.post("/course-report/{course_id}")
def email_course_report(
    course_id: int,
    to_email: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report = get_course_report(course_id, db, current_user)
    pdf_file = generate_course_report_pdf(report.model_dump())

    send_email_with_attachment(
        to_email=to_email,
        subject=f"Course Report - ID {course_id}",
        body="Attached is the course report PDF.",
        file_bytes=pdf_file.getvalue(),
        filename=f"course_report_{course_id}.pdf"
    )

    return {"message": "Course report emailed successfully"}
