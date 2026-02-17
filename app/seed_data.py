from faker import Faker
import random
from datetime import date, timedelta

from app.database import SessionLocal
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.marks import Marks
from app.core.grade_utils import calculate_grade

fake = Faker()


DEPARTMENTS = ["CSE", "IT", "ECE", "EEE", "MECH", "CIVIL", "MCA"]
YEARS = [1, 2, 3, 4]

COURSES_LIST = [
    ("MCA2601", "Python Programming", 1, 4),
    ("MCA2602", "Database Management Systems", 1, 4),
    ("MCA2603", "Operating Systems", 2, 3),
    ("MCA2604", "Computer Networks", 2, 3),
    ("MCA2605", "Software Engineering", 3, 4),
    ("MCA2606", "Web Development", 3, 3),
    ("MCA2607", "Data Structures", 1, 4),
    ("MCA2608", "Machine Learning", 4, 4),
    ("MCA2609", "Cloud Computing", 4, 3),
    ("MCA2610", "Cyber Security", 4, 3),
]

def seed_students(db, count=50):
    students = []

    for i in range(count):
        student = Student(
            name=fake.name(),
            roll_no=f"ROLL{1000+i}",
            email=fake.unique.email(),
            phone=fake.msisdn()[:10],
            dob=fake.date_of_birth(minimum_age=17, maximum_age=25),
            department=random.choice(DEPARTMENTS),
            year=random.choice(YEARS)
        )

        db.add(student)
        students.append(student)

    db.commit()
    print(f"✅ Seeded {count} students")
    return students


def seed_courses(db):
    courses = []

    for code, name,semester, credits in COURSES_LIST:
        existing = db.query(Course).filter(Course.course_code == code).first()
        if existing:
            courses.append(existing)
            continue

        course = Course(
            course_code=code,
            course_name=name,
            semester = semester,
            credits=credits
        )

        db.add(course)
        courses.append(course)

    db.commit()
    print(f"✅ Seeded {len(courses)} courses")
    return courses


def seed_enrollments(db, students, courses):
    enrollments = []

    for student in students:
        chosen_courses = random.sample(courses, k=random.randint(3, 6))

        for course in chosen_courses:
            existing = db.query(Enrollment).filter(
                Enrollment.student_id == student.id,
                Enrollment.course_id == course.id
            ).first()

            if existing:
                continue

            enrollment = Enrollment(
                student_id=student.id,
                course_id=course.id,
                enrolled_date=date.today()
            )

            db.add(enrollment)
            enrollments.append(enrollment)

    db.commit()
    print(f"✅ Seeded {len(enrollments)} enrollments")
    return enrollments


def seed_attendance(db, enrollments, days=30):
    attendance_count = 0

    for enrollment in enrollments:
        for i in range(days):
            att_date = date.today() - timedelta(days=i)

            existing = db.query(Attendance).filter(
                Attendance.student_id == enrollment.student_id,
                Attendance.course_id == enrollment.course_id,
                Attendance.attendance_date == att_date
            ).first()

            if existing:
                continue

            status = random.choices(["present", "absent"], weights=[80, 20])[0]

            attendance = Attendance(
                student_id=enrollment.student_id,
                course_id=enrollment.course_id,
                attendance_date=att_date,
                status=status
            )

            db.add(attendance)
            attendance_count += 1

    db.commit()
    print(f"✅ Seeded {attendance_count} attendance records")


def seed_marks(db, enrollments):
    marks_count = 0

    for enrollment in enrollments:
        existing = db.query(Marks).filter(
            Marks.student_id == enrollment.student_id,
            Marks.course_id == enrollment.course_id
        ).first()

        if existing:
            continue

        total_marks = 100
        marks_obtained = random.randint(25, 100)

        percentage = (marks_obtained / total_marks) * 100
        grade, grade_points = calculate_grade(percentage)

        marks = Marks(
            student_id=enrollment.student_id,
            course_id=enrollment.course_id,
            marks_obtained=marks_obtained,
            total_marks=total_marks,
            percentage=percentage,
            grade=grade,
            grade_points=grade_points
        )

        db.add(marks)
        marks_count += 1

    db.commit()
    print(f"✅ Seeded {marks_count} marks records")


def run_seed():
    db = SessionLocal()

    try:
        students = seed_students(db, count=50)
        courses = seed_courses(db)
        enrollments = seed_enrollments(db, students, courses)

        seed_attendance(db, enrollments, days=30)
        seed_marks(db, enrollments)

        print("\n🎉 DATABASE SEEDED SUCCESSFULLY!")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
