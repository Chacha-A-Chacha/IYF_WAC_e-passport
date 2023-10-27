#!/src/bin/env python3
from flask import Flask, request, render_template, flash, redirect, url_for
from .forms import ProfileForm
from ..models import db, Teacher, Student, Class, Course
from . import main
# from .utils import generate_temp_password, send_temp_password_email


@main.route("/")
def main():


    return render_template("student_dashboard.html")


@main.route('/dashboard/<int:student_id>', methods=['GET'])
def student_dashboard(student_id):
    # Fetch student information including QR code data and profile photo
    student = Student.query.get(student_id)

    # If student not found, you might want to handle this scenario, e.g., redirect to an error page

    # Pass student information to the template
    return render_template('students/dashboard.html', student=student)

@main.route("/")
def dashboard():
    # Get the student ID from the session (replace 'student_id' with the actual key you use in the session)
    student_id = session.get('student_id')

    # Check if the student is logged in (you might want to add additional authentication checks)
    if student_id:
        # Fetch student information from the database based on the student_id
        student = Student.query.filter_by(id=student_id).first()

        # Fetch additional information related to the student (modify queries based on your models and relationships)
        courses_enrolled = Course.query.filter_by(student_id=student.id).all()
        class_schedule = ClassSchedule.query.filter_by(student_id=student.id).all()
        assignments = Assignment.query.filter_by(student_id=student.id).all()
        grades = Grade.query.filter_by(student_id=student.id).all()
        attendance_records = Attendance.query.filter_by(student_id=student.id).all()

        # Pass student and related information to the template
        return render_template('students/dashboard.html', student=student, 
                               courses_enrolled=courses_enrolled, class_schedule=class_schedule, 
                               assignments=assignments, grades=grades, attendance_records=attendance_records)
    else:
        # Handle the case when no student is logged in (redirect to login page or display an error)
        return "Unauthorized access", 401  # Return a 401 Unauthorized status code

# Add more routes and functionality as needed

@main.route("/")
def profile():

    """
    The profile page allows users to view and edit their own information.
    
    """

    pass

@main.route("/")
def edit_profile():

    pass

