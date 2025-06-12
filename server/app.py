from flask import Flask
from flask_migrate import Migrate
from models import db, Student, Grade, Subject


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://dbadmin:adm1n1234@localhost:5432/school"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/grades')
def get_grades():
    grades = Grade.query.all()
    return [g.to_dict() for g in grades], 200

if __name__ == '__main__':
    app.run(debug=True, port=5555)