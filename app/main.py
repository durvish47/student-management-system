from fastapi import FastAPI,Depends
from app.database import engine
from app import models
from fastapi.responses import FileResponse
from app.routers.auth_router import router as auth_router
from app.core.auth_dependency import get_current_user
from app.routers.student_router import router as student_router
from app.routers.course_router import router as course_router
from app.routers.enrollment_router import router as enrollment_router
from app.routers.attendance_router import router as attendance_router
from app.routers.marks_router import router as marks_router
from app.routers.report_router import router as report_router
from app.routers.course_report_router import router as course_report_router
from app.routers.department_report_router import router as department_report_router
from app.routers.leaderboard_router import router as leaderboard_router
from app.routers.defaulters_router import router as defaulters_router
from app.routers.export_router import router as export_router
from app.routers.email_router import router as email_router
from app.routers.at_risk_router import router as at_risk_router

app = FastAPI(title="Student Management System API")
app.include_router(auth_router)
app.include_router(student_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(attendance_router)
app.include_router(marks_router)
app.include_router(report_router)
app.include_router(course_report_router)
app.include_router(department_report_router)
app.include_router(leaderboard_router)
app.include_router(defaulters_router)
app.include_router(export_router)
app.include_router(email_router)
app.include_router(at_risk_router)

models.Base.metadata.create_all(bind=engine)
 
@app.get("/")
def home():
    return {"message": "Student Management System API runs successfully!"}

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return FileResponse("favicon.ico")

@app.get("/api/protected")
def protected_route(current_user=Depends(get_current_user)):
    return{
        "message":"You are Authorised",
        "user_id":current_user.id,
        "role": current_user.role
    }