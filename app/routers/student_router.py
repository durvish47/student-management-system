from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session # type: ignore
from app.database import get_db
from app.models.student import Student
from app.schemas.student_schema import StudentCreate, StudentResponse, StudentUpdate
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/api/students", tags=["Students"])

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):

    existing = db.query(Student).filter(Student.roll_no == student.roll_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Roll no already exists")
    
    new_student = Student(
        name = student.name,
        roll_no = student.roll_no,
        email = student.email,
        phone = student.phone,
        dob = student.dob,
        department = student.department,
        year = student.year
        )
    
    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@router.get("/", response_model=list[StudentResponse])
def get_all_students(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    students = db.query(Student).all()
    return students

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate ,db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    update_data = student.model_dump(exclude_unset=True)
    print("UPDATE FUNCTION CALLED", update_data)
    for key, value in update_data.items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student

@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):

    db_student = db.query(Student).filter(Student.id == student_id).first()

    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    db.delete(db_student)
    db.commit()

    return {"messsage": "Student deleted successfully"}