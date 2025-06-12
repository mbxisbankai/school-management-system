from app import app
from models import db, Student, Subject, Grade

# Sample data
students_data = [
    {"name": "Alice", "age": 20},
    {"name": "Bob", "age": 22},
    {"name": "Charlie", "age": 21}
]

subjects_data = [
    {"name": "Mathematics"},
    {"name": "Physics"},
    {"name": "Chemistry"}
]

grades_data = [
    {"student_name": "Alice", "subject_name": "Mathematics", "grade": "A"},
    {"student_name": "Alice", "subject_name": "Physics", "grade": "B"},
    {"student_name": "Bob", "subject_name": "Mathematics", "grade": "C"},
    {"student_name": "Charlie", "subject_name": "Chemistry", "grade": "A"},
]

with app.app_context():
    print("🌱 Seeding database...")

    # Reset the database
    db.drop_all()
    db.create_all()

    # Create subjects
    subjects = {}
    for data in subjects_data:
        subject = Subject(name=data["name"])
        db.session.add(subject)
        subjects[data["name"]] = subject

    # Create students
    students = {}
    for data in students_data:
        student = Student(name=data["name"], age=data["age"])
        db.session.add(student)
        students[data["name"]] = student

    db.session.commit()

    # Associate students with subjects and assign grades
    for data in grades_data:
        student = students[data["student_name"]]
        subject = subjects[data["subject_name"]]

        # Many-to-many linking
        student.subjects.append(subject)

        # Create grade
        grade = Grade(student=student, subject=subject, grade=data["grade"])
        db.session.add(grade)

    db.session.commit()

    print("Done seeding!")
