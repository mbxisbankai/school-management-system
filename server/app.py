from flask import Flask
from flask_migrate import Migrate
from models import db, Student, Grade, Subject
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Welcome to the School Management System</h1>'

@app.route('/students')
def students():
    students = Student.query.all()
    return [s.to_dict() for s in students], 200

@app.route('/students/<int:id>')
def find_student_by_id(id):
    student = Student.query.filter(Student.id == id).first()
    if not student:
        return {'error': 'Student not found'}, 404
    else:
        return student.to_dict(), 200

@app.route('/subjects')
def get_subjects():
    subjects = Subject.query.all()
    return [sub.to_dict() for sub in subjects], 200

@app.route('/subjects/<int:id>')
def find_subject_by_id(id):
    subject = Subject.query.filter(Subject.id == id).first()
    if not subject:
        return {'error': 'Subject not found'}, 404
    else:
        return subject.to_dict(), 200

@app.route('/grades')
def get_grades():
    grades = Grade.query.all()
    return [g.to_dict() for g in grades], 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)