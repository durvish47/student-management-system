from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.course import Course
from app.schemas.course_schema import CourseCreate, CourseUpdate, CourseResponse
from app.core.auth_dependency import get_current_user

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=CourseResponse)
def create_course(course: CourseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing = db.query(Course).filter(Course.course_code == course.course_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")
    
    new_course = Course(
        course_code=course.course_code,
        course_name=course.course_name,
        semester=course.semester,
        credits=course.credits
    )

    db.add(new_course)
    db.commit()
    db.refresh(new_course)

    return new_course

@router.get("/", response_model=list[CourseResponse])
def get_all_courses(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Course).all()

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return course

@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_course = db.query(Course).filter(Course.id == course_id).first()

    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    update_data = course.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)

    return db_course

@router.delete("/{course_id}")
def delete_course(course_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")

    db.delete(db_course)
    db.commit()

    return {"message": "Course deleted successfully"}
    