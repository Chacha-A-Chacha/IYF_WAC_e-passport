#!/usr/bin/env python3
from flask_login import  UserMixin
from datetime import datetime  # Import the datetime module
import random
import string
import qrcode
# from PIL import Image
from io import BytesIO


from . import db, login_manager, bcrypt


# Create a user loader function that Flask-Login will use to load users from the database.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
        Represents a user in the system.

        Attributes:
            id (int): The unique identifier of the user.
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The hashed password of the user.
            date_of_birth (date): The date of birth of the user.
            passport_photo_filename (str): The filename of the user's passport photo.
            nationality (str): The nationality of the user.
            phone_number (str): The phone number of the user.
            role (str): The role of the user ('admin', 'teacher', or 'student').

        Relationships:
            class_enrollment (Class): Many-to-one relationship with the Class table representing the class the student is enrolled in.
            courses (Course): One-to-many relationship with the Course table representing the courses the user is associated with.
            attendances (Attendance): One-to-many relationship with the Attendance table representing the attendances of the user.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Added email field
    password = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date)
    passport_photo_filename = db.Column(db.String(255))
    nationality = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    role = db.Column(db.String(50), nullable=False)  # Role can be 'admin', 'teacher', 'student'
    courses = db.relationship('Course', backref='teacher', lazy=True)  # One-to-many relationship with courses

    # For students, many-to-one relationship with classes
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)
    class_ = db.relationship('Class', foreign_keys=[class_id])

    def __init__(self, username, email, password, role):
        """
        Initializes a new User object.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str): The hashed password of the user.
            role (str): The role of the user ('admin', 'teacher', or 'student').
        """
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hashing the password
        self.role = role

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)


class Course(db.Model):
    """
       Represents a course in the system.

       Attributes:
           id (int): The unique identifier of the course.
           course_name (str): The name of the course.

       Relationships:
           teacher (User): One-to-one relationship with the User table representing the teacher of the course.
           classes (Class): One-to-many relationship with the Class table representing the classes in the course.
    """
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(120), unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    classes = db.relationship('Class', backref='course', lazy=True)  # One-to-many relationship with classes


class Class(db.Model):
    """
        Represents a class in the system.

        Attributes:
            id (int): The unique identifier of the class.
            class_name (str): The name of the class.

        Relationships:
            course (Course): Many-to-one relationship with the Course table representing the course the class belongs to.
            teacher (User): One-to-one relationship with the User table representing the teacher of the class.
            students (User): One-to-many relationship with the User table representing the students in the class.
            attendances (Attendance): One-to-many relationship with the Attendance table representing the attendances of the class.
    """
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80), unique=True, nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='class_attendance', lazy=True)  # One-to-many relationship with attendances

    # Specify the foreign key columns for the teacher relationship
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Specify the foreign key columns for the students relationship
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # Define the relationships with User model using the foreign_keys argument
    teacher = db.relationship('User', foreign_keys=[teacher_id], backref='class_taught', lazy=True)
    students = db.relationship('User', foreign_keys=[student_id], backref='class_enrollment', lazy=True)

class Teacher(User):
    """
    Represents a teacher in the system.

    Attributes:
        username (str): The username of the teacher.
        email (str): The email address of the teacher.
        password (str): The hashed password of the teacher.
        class_id (int): The ID of the class the teacher is handling.
        course_id (int): The ID of the course the teacher is teaching.

    Relationships:
        class_teacher (Class): One-to-one relationship with the Class table representing the class the teacher is handling.
        course_teacher (Course): One-to-one relationship with the Course table representing the course the teacher is teaching.
    """

    __tablename__ = 'teachers'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)

    # Specify the foreign key columns for the class_teacher relationship
    class_teacher_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)

    # Specify the foreign key columns for the course_teacher relationship
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

    # Define the relationships with Class and Course models using the foreign_keys argument
    class_teacher = db.relationship('Class', foreign_keys=[class_teacher_id], backref='teachers_in_class', lazy=True)
    course_teacher = db.relationship('Course', foreign_keys=[course_id], backref='teachers_in_course', lazy=True)


    def __init__(self, username=None, email=None, password=None, class_id=None, course_id=None):
        """
        Initializes a new Teacher object.

        Args:
            username (str): The username of the teacher.
            email (str): The email address of the teacher.
            password (str): The hashed password of the teacher.
            class_id (int): The ID of the class the teacher is handling.
            course_id (int): The ID of the course the teacher is teaching.
        """
        super().__init__(username=username, email=email, password=password, role='teacher')
        self.class_id = class_id
        self.course_id = course_id


class Attendance(db.Model):
    """
    Represents attendance records in the system.

    Attributes:
        id (int): The unique identifier of the attendance record.
        student_id (int): The ID of the student associated with the attendance record.
        class_id (int): The ID of the class associated with the attendance record.
        attendance_date (datetime): The date and time of the attendance record.
        is_present (bool): Indicates whether the student was present or absent.

    Relationships:
        class_attendance (Class): One-to-one relationship with the Class table representing the class associated with the attendance record.
    """
    __tablename__ = 'attendances'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=False)
    attendance_date = db.Column(db.DateTime, nullable=False)
    is_present = db.Column(db.Boolean, nullable=False)


class Student(User):
    """
    Represents a student in the system.

    Attributes:
        student_id (str): The unique identifier of the student.
        qr_code_image (bytes): Binary data representing the QR code image associated with the student.

    Relationships:
        attendances (Attendance): One-to-many relationship with the Attendance table representing the attendances of the student.
        class_ (Class): Many-to-one relationship with the Class table representing the class the student is enrolled in.

    """
    __tablename__ = 'students'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    qr_code_image = db.Column(db.LargeBinary, nullable=True)  # Binary field to store QR code image data
    student_class_id = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)

    # Define the relationship with the Class model
    class_ = db.relationship('Class', foreign_keys=[student_class_id])
    

    def __init__(self, name=None, email=None, school_logo_path=None, username=None, password=None):
        """
        Initializes a new Teacher object.

        Args:
            username (str): The username of the teacher.
            email (str): The email address of the teacher.
            password (str): The hashed password of the teacher.
            class_id (int): The ID of the class the teacher is handling.
            course_id (int): The ID of the course the teacher is teaching.
        """
        super().__init__(username=username, email=email, password=password, role='student')
        self.name = name
        
        self.student_id = self.generate_student_id()
        self.school_logo_path = school_logo_path
        self.generate_qr_code()

    def generate_student_id(self):
        """
        Generates a unique student ID consisting of letters and numbers.

        Returns:
           str: The generated 8-character student ID.
        """
        # Generate a unique student ID consisting of letters and numbers
        characters = string.ascii_letters + string.digits
        student_id = ''.join(random.choice(characters) for _ in range(8))  # 8-character student ID
        return student_id

    def generate_qr_code(self):
        """
        Generates a QR code containing the student ID with the school logo in the center and saves it as bytes.

        Returns:
            bytes: Binary data representing the QR code image.
        """
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

        # Open the school logo image
        # school_logo = Image.open(self.school_logo_path)

        buffer = BytesIO()
        qr_img.save(buffer)
        qr_image_bytes = buffer.getvalue()

        # Save QR code image bytes to the database
        self.qr_code_image = qr_image_bytes
