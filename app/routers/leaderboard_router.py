from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.student import Student
from app.models.marks import Marks
from app.schemas.leaderboard_schema import LeaderboardStudentResponse

router = APIRouter(prefix="/api/reports", tags=["Reports"])


@router.get("/leaderboard", response_model=list[LeaderboardStudentResponse])
def get_leaderboard(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    department: str = Query(None),
    year: int = Query(None)
):
    query = db.query(Student)

    if department:
        query = query.filter(Student.department == department)

    if year:
        query = query.filter(Student.year == year)

    students = query.all()

    leaderboard = []

    for student in students:
        marks = db.query(Marks).filter(Marks.student_id == student.id).all()

        if not marks:
            continue

        total_gp = sum(m.grade_points for m in marks)
        gpa = total_gp / len(marks)

        leaderboard.append(
            LeaderboardStudentResponse(
                student_id=student.id,
                student_name=student.name,
                roll_no=student.roll_no,
                department=student.department,
                year=student.year,
                gpa=round(gpa, 2)
            )
        )

    leaderboard.sort(key=lambda x: x.gpa, reverse=True)

    return leaderboard[:limit]
