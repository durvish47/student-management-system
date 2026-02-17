from app.database import SessionLocal
from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.attendance import Attendance
from app.models.marks import Marks


def reset_database_keep_admin():
    db = SessionLocal()

    try:
        # keep only admins
        admins = db.query(User).filter(User.role == "admin").all()

        if not admins:
            print("❌ No admin users found. Aborting reset.")
            return

        # delete all other users (teachers etc)
        db.query(User).filter(User.role != "admin").delete()

        # delete everything else
        db.query(Marks).delete()
        db.query(Attendance).delete()
        db.query(Enrollment).delete()
        db.query(Student).delete()
        db.query(Course).delete()

        db.commit()
        print("✅ Database reset complete (admin users preserved).")

    except Exception as e:
        db.rollback()
        print("❌ Reset failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    reset_database_keep_admin()
