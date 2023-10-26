#!/src/bin/env python3
from flask import Flask, request, render_template, flash, redirect, url_for
import pandas as pd
from .forms import TeacherRegistrationForm, StudentRegistrationForm
from ..models import db, Teacher, Student, Class, Course
from . import admin_bp
from .utils import generate_temp_password, send_temp_password_email


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
@admin_bp.route('/submit-excel', methods=['GET', 'POST'])
def submit_excel():
    """
    Handle the submission of an Excel file containing student data, process the data, and register students.
    Display flash messages for success or error.

    Returns:
        str: A redirect response to the admin dashboard page after processing the Excel file.
    """
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    try:
        if file:
            # Read data from Excel
            df = pd.read_excel(file)
            # Process and register students
            for index, row in df.iterrows():
                full_name = row['Full Name']
                email = row['Email']
                course = row['Course']

                # Generate student ID, temporary password, and register student
                temp_password = generate_temp_password()
                student = Student(full_name=full_name, email=email, course=course, password=temp_password)
                db.session.add(student)
                db.session.commit()

                # Send temporary password email
                send_temp_password_email(email, student.student_id, temp_password)

            flash('Students registered successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        print(str(e))  # Log the exception for debugging
        db.session.rollback()  # Rollback changes if there's an error
        flash('Error processing file. Please try again.', 'error')

    return redirect(request.url)


@admin_bp.route('/register-student', methods=['GET', 'POST'])
def admin_register_student():
    """
    Handle the registration of a new student by the admin.
    Display a registration form for the admin to input student details.
    Register the student in the database and display flash messages for success or error.

    Returns:
        str: A redirect response to the admin dashboard or the registration form page based on form submission.
    """
    form = StudentRegistrationForm()
    if form.validate_on_submit():

        try:
            username = form.username.data
            email = form.email.data
            password = generate_temp_password()
            class_name = form.class_name.data
            # additional_info = form.additional_info.data

            # Register student
            student = Student(username=username, email=email, password=password, role='student')
            # Assuming Student model has additional_info field
            # student.additional_info = additional_info
            db.session.add(student)
            db.session.commit()

            # Handle class relationship
            # Assuming Class model has appropriate relationships defined
            class_obj = Class.query.filter_by(class_name=class_name).first()
            student.class_enrollment = class_obj
            db.session.commit()

            # Send temporary password email
            send_temp_password_email(email, student.student_id, password)

            flash('Student registered successfully!', 'success')
            return redirect(url_for('admin_bp.admin_dashboard'))
        except Exception as e:
            print(str(e))  # Log the exception for debugging
            db.session.rollback()  # Rollback changes if there's an error
            flash('Error registering student. Please try again.', 'error')

    return redirect(url_for('admin.register'))


@admin_bp.route('/register-teacher', methods=['GET', 'POST'])
def admin_register_teacher():
    """
    Handle the registration of a new teacher by the admin.
    Display a registration form for the admin to input teacher details.
    Register the teacher in the database and display flash messages for success or error.

    Returns:
        str: A redirect response to the admin dashboard or the registration form page based on form submission.
    """
    form = TeacherRegistrationForm()
    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            password = generate_temp_password()  # Generate temporary password
            class_name = form.class_name.data
            course_name = form.course_name.data

            # Register teacher
            teacher = Teacher(username=username, email=email, password=password, role='teacher')
            db.session.add(teacher)
            db.session.commit()

            # Handle class and course relationships
            # Assuming Class and Course models have appropriate relationships defined
            class_obj = Class.query.filter_by(class_name=class_name).first()
            course_obj = Course.query.filter_by(course_name=course_name).first()
            teacher.class_teacher = class_obj
            teacher.course_teacher = course_obj
            db.session.commit()

            # Send temporary password email
            send_temp_password_email(email, teacher.teacher_id, password)

            flash('Teacher registered successfully!', 'success')
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            print(str(e))  # Log the exception for debugging
            db.session.rollback()  # Rollback changes if there's an error
            flash('Error registering teacher. Please try again.', 'error')

    return redirect(url_for('admin.register'))


# Helper function to generate a student ID
# def generate_student_id(full_name):
#     # Generate student ID based on full name (customize as needed)
#     # Example: Extract first letters of first name and last name, and add random numbers
#     return ''.join(word[0].upper() for word in full_name.split()) + ''.join(str(random.randint(0, 9)) for _ in range(4))


# Helper function to generate a temporary password
# def generate_temp_password():
#     # Generate a random temporary password (customize as needed)
#     # Example: Generate a random string of length 8
#     return ''.join(random.choices(string.ascii_letters + string.digits, k=8))


# Helper function to send registration email
# def send_registration_email(email, student_id, temp_password):
#     msg = Message('Your Student ID and Temporary Password',
#                   sender='your-email@example.com', recipients=[email])
#     msg.body = f'Your Student ID: {student_id}\nTemporary Password: {temp_password}\nPlease reset your password after login.'
#     mail.send(msg)


@admin_bp.route('/register')
def register():
    student_form = StudentRegistrationForm()
    teacher_form = TeacherRegistrationForm()
    # Retrieve registered students from the database (modify this query based on your actual model)
    # students = Student.query.all()
    return render_template('admin/register.html', teacher_form=teacher_form, student_form=student_form)


# Admin route to display registered students
@admin_bp.route('/students')
def admin_students():
    # Retrieve registered students from the database (modify this query based on your actual model)
    students = Student.query.all()
    return render_template('students.html', students=students)

#
# @admin_bp.route('/teachers')
# def admin_teachers():
#     # Retrieve registered students from the database (modify this query based on your actual model)
#     teachers = Teacher.query.all()
#     return render_template('teachers.html', teachers=teachers)