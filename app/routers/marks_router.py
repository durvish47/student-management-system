from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth_dependency import get_current_user
from app.database import get_db
from app.models.enrollment import Enrollment
from app.models.marks import Marks
from app.schemas.marks_schema import MarkCreate, MarkUpdate ,MarkResponse
from app.core.grade_utils import calculate_grade

router = APIRouter(prefix="/api/marks", tags=["Marks"])

@router.post("/", response_model=MarkResponse)
def add_marks(marks: MarkCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    
    enrolled = db.query(Enrollment).filter(
        Enrollment.student_id == marks.student_id,
        Enrollment.course_id == marks.course_id
    ).first()

    if not enrolled:
        raise HTTPException(status_code=400, detail="Student is not enrolled in this course")
    
    existing = db.query(Marks).filter(
        Marks.student_id == marks.student_id,
        Marks.course_id == marks.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Marks already added for this course")
    
    percentage = (marks.marks_obtained / marks.total_marks) * 100
    grade, grade_points = calculate_grade(percentage)

    new_marks = Marks(
        student_id = marks.student_id,
        course_id = marks.course_id,
        marks_obtained = marks.marks_obtained,
        total_marks = marks.total_marks,
        percentage = percentage,
        grade = grade,
        grade_points = grade_points
    )

    db.add(new_marks)
    db.commit()

    db.refresh(new_marks)

    return new_marks

@router.get("/", response_model=list[MarkResponse])
def get_all_marks(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Marks).all()

@router.get("/student/{student_id}", response_model=list[MarkResponse])
def get_marks_by_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Marks).filter(Marks.student_id == student_id).all()

@router.get("/course/{course_id}", response_model=list[MarkResponse])
def get_marks_by_course(course_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Marks).filter(Marks.course_id == course_id).all()

@router.put("/{marks_id}", response_model=MarkResponse)
def update_marks(marks_id: int, mark: MarkUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    db_marks = db.query(Marks).filter(Marks.id == marks_id).first()

    if not db_marks:
        raise HTTPException(status_code=404, detail="Marks record not found")
    
    update_data = mark.model_dump(exclude_unset=True)

    if "marks_obtained" in update_data:
        db_marks.marks_obtained = update_data["marks_obtained"]

    if "total_marks" in update_data:
        db_marks.total_marks = update_data["total_marks"]

    db_marks.percentage = (db_marks.marks_obtained / db_marks.total_marks) * 100
    db_marks.grade, db_marks.grade_points = calculate_grade(db_marks.percentage)

    db.commit()
    db.refresh(db_marks)

    return db_marks

@router.delete("/{marks_id}")
def delete_marks(marks_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    db_marks = db.query(Marks).filter(Marks.id == marks_id).first()

    if not db_marks:
        raise HTTPException(status_code=404, detail="Marks record not found")
    
    db.delete(db_marks)
    db.commit()

    return {"message": "Marks deleted successfully"}