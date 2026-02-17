def calculate_grade(percentage: float):
    if percentage >= 90:
        return "A+", 10
    elif percentage >= 80:
        return "A", 9
    elif percentage >= 70:
        return "B+", 8
    elif percentage >= 60:
        return "B", 7
    elif percentage >= 50:
        return "C", 6
    elif percentage >= 40:
        return "D", 5
    else:
        return "F", 0