from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user

from app.routers.report_router import get_student_report
from app.routers.leaderboard_router import get_leaderboard
from app.routers.defaulters_router import get_attendance_defaulters

from app.utils.pdf_generator import generate_student_report_pdf
from app.utils.excel_generator import generate_leaderboard_excel, generate_defaulters_excel
from app.routers.course_report_router import get_course_report
from app.utils.pdf_generator import generate_course_report_pdf


router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/student-report/pdf/{student_id}")
def export_student_report_pdf(
    student_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report = get_student_report(student_id, db, current_user)
    pdf_file = generate_student_report_pdf(report.model_dump())

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=student_report_{student_id}.pdf"}
    )


@router.get("/leaderboard/excel")
def export_leaderboard_excel(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    leaderboard = get_leaderboard(db=db, current_user=current_user)
    excel_file = generate_leaderboard_excel([s.model_dump() for s in leaderboard])

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=leaderboard.xlsx"}
    )


@router.get("/defaulters/excel")
def export_defaulters_excel(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    defaulters = get_attendance_defaulters(db=db, current_user=current_user, limit=50)
    excel_file = generate_defaulters_excel([d.model_dump() for d in defaulters])

    return StreamingResponse(
        excel_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=defaulters.xlsx"}
    )

@router.get("/course-report/pdf/{course_id}")
def export_course_report_pdf(
    course_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    report = get_course_report(course_id, db, current_user)
    pdf_file = generate_course_report_pdf(report.model_dump())

    return StreamingResponse(
        pdf_file,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=course_report_{course_id}.pdf"}
    )
