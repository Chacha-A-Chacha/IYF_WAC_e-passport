#!/src/bin/env python3
from flask import Flask, request, render_template
import pandas as pd
from app import db  # Import db from the main __init__.py file
from ..models import User, Student
from . import admin_bp


# Student model (example)
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.String(20), unique=True, nullable=False)
#     full_name = db.Column(db.String(120), nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     course = db.Column(db.String(80), nullable=False)
#     password = db.Column(db.String(120), nullable=False)  # Hashed password stored in the database


@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    """

    """
    # Logic to fetch admin-related data from the database or other sources
    admin_data = {
        'total_users': 1000,
        'total_orders': 500,
        'new_requests': 10
    }
    # Render the admin dashboard template and pass the admin data to it
    return render_template('admin/admin_dashboard.html', admin_data=admin_data)


# Route to submit the Excel sheet and register students
@admin_bp.route('/submit-excel', methods=['POST'])
def submit_excel():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    if file:
        # Read data from Excel
        df = pd.read_excel(file)
        # Process and register students
        for index, row in df.iterrows():
            full_name = row['Full Name']
            email = row['Email']
            course = row['Course']

            # Generate student ID, temporary password, and register student
            # student_id = generate_student_id(full_name)
            temp_password = generate_temp_password()
            student = Student(full_name=full_name, email=email, course=course,
                              password=temp_password)
            db.session.add(student)
            db.session.commit()
        return "Students registered successfully!"

    return "Error processing file"


# Helper function to generate a student ID
# def generate_student_id(full_name):
#     # Generate student ID based on full name (customize as needed)
#     # Example: Extract first letters of first name and last name, and add random numbers
#     return ''.join(word[0].upper() for word in full_name.split()) + ''.join(str(random.randint(0, 9)) for _ in range(4))


# Helper function to generate a temporary password
def generate_temp_password():
    # Generate a random temporary password (customize as needed)
    # Example: Generate a random string of length 8
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# Helper function to send registration email
def send_registration_email(email, student_id, temp_password):
    msg = Message('Your Student ID and Temporary Password',
                  sender='your-email@example.com', recipients=[email])
    msg.body = f'Your Student ID: {student_id}\nTemporary Password: {temp_password}\nPlease reset your password after login.'
    mail.send(msg)


# Admin route to display registered students
@admin_bp.route('/students')
def admin_students():
    # Retrieve registered students from the database (modify this query based on your actual model)
    students = Student.query.all()
    return render_template('students.html', students=students)
