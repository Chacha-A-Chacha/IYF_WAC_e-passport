
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
import random
import string
import qrcode
from PIL import Image
from io import BytesIO


from . import db, login_manager, bcrypt


# Create a user loader function that Flask-Login will use to load users from the database.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Added email field
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Role can be 'admin', 'teacher', 'student'
    courses = db.relationship('Course', backref='teacher', lazy=True)  # One-to-many relationship with courses

    # For students, many-to-one relationship with classes
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hashing the password
        self.role = role

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    classes = db.relationship('Class', backref='course', lazy=True)  # One-to-many relationship with classes


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    students = db.relationship('User', backref='class_enrollment', lazy=True)  # One-to-many relationship with students
    attendances = db.relationship('Attendance', backref='class_attendance', lazy=True)  # One-to-many relationship with attendances


class Attendance(db.Model):
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    attendance_date = db.Column(db.DateTime, nullable=False)
    is_present = db.Column(db.Boolean, nullable=False)


class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    qr_code_image = db.Column(db.LargeBinary, nullable=True)  # Binary field to store QR code image data

    def __init__(self, name=None, school_logo_path=None, username=None, password=None):
        super().__init__(username=username, password=password, role='student')
        self.name = name
        self.student_id = self.generate_student_id()
        self.school_logo_path = school_logo_path
        self.generate_qr_code()

    def generate_student_id(self):
        # Generate a unique student ID consisting of letters and numbers
        characters = string.ascii_letters + string.digits
        student_id = ''.join(random.choice(characters) for _ in range(8))  # 8-character student ID
        return student_id

    def generate_qr_code(self):
        # Generate QR code containing the student ID with the school logo in the center
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.student_id)
        qr.make(fit=True)

        # Create an in-memory buffer to save QR code as bytes
        qr_img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_img.save(buffer)
        qr_image_bytes = buffer.getvalue()

        # Save QR code image bytes to the database
        self.qr_code_image = qr_image_bytes
