from openpyxl import Workbook
from io import BytesIO


def generate_leaderboard_excel(data: list) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Leaderboard"

    ws.append(["Student ID", "Name", "Roll No", "Department", "Year", "GPA"])

    for student in data:
        ws.append([
            student["student_id"],
            student["student_name"],
            student["roll_no"],
            student["department"],
            student["year"],
            student["gpa"]
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return buffer


def generate_defaulters_excel(data: list) -> BytesIO:
    wb = Workbook()
    ws = wb.active
    ws.title = "Defaulters"

    ws.append(["Student ID", "Name", "Roll No", "Department", "Year", "Attendance %"])

    for student in data:
        ws.append([
            student["student_id"],
            student["student_name"],
            student["roll_no"],
            student["department"],
            student["year"],
            student["attendance_percentage"]
        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return buffer
