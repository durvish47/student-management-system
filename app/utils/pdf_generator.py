from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO


def generate_student_report_pdf(report_data: dict) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Student Report")
    y -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Student Name: {report_data['student_name']}")
    y -= 20
    pdf.drawString(50, y, f"Roll No: {report_data['roll_no']}")
    y -= 20
    pdf.drawString(50, y, f"Department: {report_data['department']}")
    y -= 20
    pdf.drawString(50, y, f"Year: {report_data['year']}")
    y -= 20
    pdf.drawString(50, y, f"GPA: {report_data['gpa']}")
    y -= 40

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Courses:")
    y -= 25

    pdf.setFont("Helvetica", 10)

    for course in report_data["courses"]:
        if y < 100:
            pdf.showPage()
            y = height - 50

        pdf.drawString(50, y, f"Course Code: {course['course_code']}")
        y -= 15
        pdf.drawString(50, y, f"Attendance: {course['attendance_percentage']}%")
        y -= 15
        pdf.drawString(50, y, f"Marks: {course['marks_obtained']} / {course['total_marks']}")
        y -= 15
        pdf.drawString(50, y, f"Grade: {course['grade']}  GP: {course['grade_points']}")
        y -= 25

    pdf.save()
    buffer.seek(0)

    return buffer

def generate_course_report_pdf(report_data: dict) -> BytesIO:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    y = height - 50

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, "Course Report")
    y -= 30

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, y, f"Course Name: {report_data['course_name']}")
    y -= 20
    pdf.drawString(50, y, f"Course Code: {report_data['course_code']}")
    y -= 20
    pdf.drawString(50, y, f"Semester: {report_data['semester']}")
    y -= 20
    pdf.drawString(50, y, f"Credits: {report_data['credits']}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Summary:")
    y -= 20

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Total Students Enrolled: {report_data['total_students']}")
    y -= 20
    pdf.drawString(50, y, f"Total Classes Conducted: {report_data['total_classes']}")
    y -= 20
    pdf.drawString(50, y, f"Average Attendance: {report_data['avg_attendance_percentage']}%")
    y -= 20

    if report_data.get("avg_marks_percentage") is not None:
        pdf.drawString(50, y, f"Average Marks: {report_data['avg_marks_percentage']}%")
        y -= 20

    if report_data.get("avg_grade_points") is not None:
        pdf.drawString(50, y, f"Average Grade Points: {report_data['avg_grade_points']}")
        y -= 20

    y -= 20

    topper = report_data.get("topper")
    if topper:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(50, y, "Topper:")
        y -= 20

        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, y, f"Name: {topper['student_name']}")
        y -= 20
        pdf.drawString(50, y, f"Roll No: {topper['roll_no']}")
        y -= 20
        pdf.drawString(50, y, f"Grade: {topper['grade']}")
        y -= 20
        pdf.drawString(50, y, f"Grade Points: {topper['grade_points']}")
        y -= 20

    pdf.save()
    buffer.seek(0)
    return buffer