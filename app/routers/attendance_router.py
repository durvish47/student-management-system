from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.attendance import Attendance
from app.models.enrollment import Enrollment
from app.schemas.attendance_schema import AttendanceCreate, AttendanceUpdate, AttendanceResponse

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])

@router.post("/", response_model=AttendanceResponse)
def mark_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if attendance.attendance_date is None:
        attendance.attendance_date = date.today()

    enrolled = db.query(Enrollment).filter(
        Enrollment.student_id == attendance.student_id,
        Enrollment.course_id == attendance.course_id
    ).first()

    if not enrolled:
        raise HTTPException(status_code=400, detail="Student is not enrolled in the course")
    
    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.course_id == attendance.course_id,
        Attendance.attendance_date == attendance.attendance_date
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for this date")
    
    new_attendance = Attendance(
        student_id = attendance.student_id,
        course_id = attendance.course_id,
        attendance_date = attendance.attendance_date,
        status = attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)

    return new_attendance

@router.get("/", response_model=list[AttendanceResponse])
def get_all_attendance(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Attendance).all()

@router.get("/student/{student_id}", response_model=list[AttendanceResponse])
def get_attendance_by_student(student_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()

@router.get("/course/{course_id}", response_model=list[AttendanceResponse])
def get_attendance_by_course(course_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Attendance).filter(Attendance.course_id == course_id).all()

@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(attendance_id: int, attendance: AttendanceUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not db_attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    db_attendance.status = attendance.status

    db.commit()
    db.refresh(db_attendance)

    return db_attendance

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()

    if not db_attendance:
        raise(HTTPException(status_code=404, detail="Attendance not found"))
    
    db.delete(db_attendance)
    db.commit()

    return{"message": "Attendance deleted successfully"}