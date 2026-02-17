# 🎓 Student Management System Backend (FastAPI + MySQL)

A complete backend system built using **FastAPI**, **SQLAlchemy**, and **MySQL** for managing students, courses, enrollments, attendance, marks, GPA analytics, reporting, exporting, and email-based report delivery.

---

## 🚀 Features

### 🔐 Authentication
- Admin login/register
- JWT Token-based authentication
- Protected APIs using dependency injection

### 👨‍🎓 Student Management
- Add students
- Update students
- Delete students
- List students

### 📚 Course Management
- Add courses
- Update courses
- Delete courses
- List courses

### 📝 Enrollment Module
- Enroll students into courses
- Prevent duplicate enrollment
- View enrollments

### 📅 Attendance Module
- Mark attendance for students
- Prevent duplicate attendance on same date
- View attendance by student/course

### 🧾 Marks Module (with Grade & Grade Points)
- Add marks
- Auto calculate:
  - Percentage
  - Grade
  - Grade Points
- Update marks and recalculate grade
- GPA support

### 📊 Reports Module
- Student report (attendance + marks + GPA)
- Course report
- Leaderboard report

### 📤 Export Module
- Export leaderboard as Excel
- Export student report as PDF

### 📧 Email Module
- Send student report PDF to email using Gmail SMTP
- Uses Gmail App Password

### 📈 Analytics Module
- GPA-based leaderboard
- Students at risk (low GPA + attendance)
- Course performance analysis

### 🌱 Seed Module
- Seed random students, courses, enrollments, marks, attendance
- Useful for demo/live testing

### 🐳 Docker Support
- MySQL + FastAPI backend using docker-compose

---

## 🛠 Tech Stack

- **FastAPI**
- **SQLAlchemy ORM**
- **MySQL**
- **Pydantic**
- **JWT Authentication**
- **Docker + Docker Compose**
- **OpenPyXL (Excel Export)**
- **ReportLab (PDF Export)**
- **SMTP (Email)**

---

## 📂 Project Folder Structure

student-management-system/
│
├── app/
│ ├── core/
│ │ ├── security.py
│ │ ├── auth_dependency.py
│ │ ├── grade_utils.py
│ │
│ ├── models/
│ │ ├── student.py
│ │ ├── course.py
│ │ ├── enrollment.py
│ │ ├── attendance.py
│ │ ├── marks.py
│ │ ├── admin.py
│ │
│ ├── routers/
│ │ ├── auth_router.py
│ │ ├── student_router.py
│ │ ├── course_router.py
│ │ ├── enrollment_router.py
│ │ ├── attendance_router.py
│ │ ├── marks_router.py
│ │ ├── report_router.py
│ │ ├── leaderboard_router.py
│ │ ├── export_router.py
│ │ ├── email_router.py
│ │ ├── analytics_router.py
│ │
│ ├── schemas/
│ │ ├── student_schema.py
│ │ ├── course_schema.py
│ │ ├── enrollment_schema.py
│ │ ├── attendance_schema.py
│ │ ├── marks_schema.py
│ │ ├── report_schema.py
│ │ ├── leaderboard_schema.py
│ │
│ ├── utils/
│ │ ├── email_sender.py
│ │ ├── pdf_generator.py
│ │
│ ├── database.py
│ ├── main.py
│ ├── seed_data.py
│
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
├── .env
├── .env.example
└── README.md


---

## ⚙️ Installation & Setup (Local)

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/student-management-system.git
cd student-management-system
2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate     # Linux/Mac
venv\Scripts\activate        # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Configure Environment Variables
Create .env file and add values:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=student_db

SECRET_KEY=your_secret_key

SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
▶️ Run Application
uvicorn app.main:app --reload
Server runs at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs

🌱 Seed Random Data
python -m app.seed_data
This will seed:

Students

Courses

Enrollments

Attendance

Marks

🔑 Authentication Usage
Login Endpoint
POST /api/auth/login

After login, Swagger will return:

{
  "access_token": "xxxxx",
  "token_type": "bearer"
}
Use this token in Swagger Authorize:

Bearer <token>
📌 API Endpoints Summary
Auth
POST /api/auth/register

POST /api/auth/login

Students
GET /api/students/

POST /api/students/

PUT /api/students/{id}

DELETE /api/students/{id}

Courses
GET /api/courses/

POST /api/courses/

PUT /api/courses/{id}

DELETE /api/courses/{id}

Enrollment
POST /api/enrollments/

GET /api/enrollments/

GET /api/enrollments/student/{student_id}

GET /api/enrollments/course/{course_id}

Attendance
POST /api/attendance/

GET /api/attendance/

GET /api/attendance/student/{student_id}

GET /api/attendance/course/{course_id}

PUT /api/attendance/{attendance_id}

DELETE /api/attendance/{attendance_id}

Marks
POST /api/marks/

GET /api/marks/

GET /api/marks/student/{student_id}

GET /api/marks/course/{course_id}

PUT /api/marks/{marks_id}

DELETE /api/marks/{marks_id}

Reports
GET /api/reports/student/{student_id}

GET /api/reports/course/{course_id}

GET /api/reports/leaderboard

Export
GET /api/export/leaderboard/excel

GET /api/export/student-report/{student_id}/pdf

Email
POST /api/email/student-report/{student_id}?to_email=example@gmail.com

Analytics
GET /api/analytics/students-at-risk

GET /api/analytics/course-performance/{course_id}

GET /api/analytics/overall-summary

📧 Gmail SMTP Setup
To use Gmail SMTP, you must generate an App Password:

Enable 2-Step Verification in Google Account

Go to App Passwords

Generate password for "Mail"

Use that password in .env

Example:

SMTP_EMAIL=your_email@gmail.com
SMTP_PASSWORD=xxxx xxxx xxxx xxxx
🐳 Docker Deployment (Local)
Run using docker compose
docker compose up --build
Backend will run on:

http://localhost:8000

MySQL will run on:

localhost:3307

🔥 Notes
All APIs are protected except login/register

Attendance prevents duplicates for same date

Marks module automatically calculates grade & GPA

Leaderboard is GPA based

📌 Future Enhancements
Frontend React Dashboard

Admin role permissions

Student login support

Advanced analytics charts

Notifications system

👨‍💻 Author
Developed by Durvish 🚀


---