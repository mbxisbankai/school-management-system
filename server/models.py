from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Integer, String, Table, ForeignKey
from sqlalchemy_serializer import SerializerMixin

# Naming convention to avoid alembic migration conflicts
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Many-to-many association table
student_subject = Table(
    'student_subject', db.Model.metadata,
    db.Column('student_id', Integer, ForeignKey('students.id'), primary_key=True),
    db.Column('subject_id', Integer, ForeignKey('subjects.id'), primary_key=True)
)

class Student(db.Model, SerializerMixin):
    __tablename__ = "students"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, nullable=False)
    age = db.Column(Integer)

    # Relationships
    subjects = db.relationship('Subject', secondary=student_subject, back_populates='students')
    grades = db.relationship('Grade', back_populates='student', cascade="all, delete-orphan")

    serialize_rules = ('-subjects.students', '-grades')

    def __repr__(self):
        return f'<Student {self.id}: {self.name}, {self.age}>'

class Subject(db.Model, SerializerMixin):
    __tablename__ = "subjects"

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String, unique=True, nullable=False)

    # Relationships
    students = db.relationship('Student', secondary=student_subject, back_populates='subjects')
    grades = db.relationship('Grade', back_populates='subject', cascade="all, delete-orphan")

    serialize_rules = ('-students.subjects', '-grades')

    def __repr__(self):
        return f'<Subject {self.id}: {self.name}>'

class Grade(db.Model, SerializerMixin):
    __tablename__ = "grades"

    id = db.Column(Integer, primary_key=True)
    grade = db.Column(String(2), nullable=False)

    student_id = db.Column(Integer, ForeignKey('students.id'))
    subject_id = db.Column(Integer, ForeignKey('subjects.id'))

    student = db.relationship('Student', back_populates='grades')
    subject = db.relationship('Subject', back_populates='grades')

    # Optional: Prevent duplicate grade entries for the same student-subject pair
    __table_args__ = (
        db.UniqueConstraint('student_id', 'subject_id', name='unique_student_subject_grade'),
    )

    serialize_rules = ('-student', '-subject') 

    def __repr__(self):
        return f'<Grade {self.grade}: Student {self.student_id}, Subject {self.subject_id}>'
