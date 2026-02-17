from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.auth_dependency import get_current_user
from app.models.enrollment import Enrollment
from app.models.student import Student
from app.models.course import Course
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("/", response_model=EnrollmentResponse)
def enroll_student(enrollment: EnrollmentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    course = db.query(Course).filter(Course.id == enrollment.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment.student_id,
        Enrollment.course_id == enrollment.course_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Student is already enrolled in this course")

    new_enrollment = Enrollment(
        student_id = enrollment.student_id,
        course_id = enrollment.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return new_enrollment

@router.get("/student/{student_id}", response_model=list[EnrollmentResponse])
def get_courses_of_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()

@router.get("/courses/{course_id}", response_model=list[EnrollmentResponse])
def get_students_of_course(course_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Enrollment).filter(Enrollment.course_id == course_id).all()

@router.delete("/{enrollment_id}", response_model=list[EnrollmentResponse])
def delete_enrollment(enrollment_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()

    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    db.delete(enrollment)
    db.commit()

    return {"message": "Enrollment deleted successfully"}

