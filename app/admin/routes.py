#!/src/bin/env python3
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from sqlalchemy.exc import IntegrityError
import pandas as pd

from .forms import TeacherRegistrationForm, StudentRegistrationForm
from ..models import db, Teacher, Student, Class, Course
from . import admin_bp
from .utils import generate_temp_password, send_temp_password_email


@admin_bp.route('/admin_dashboard')
def admin_dashboard():
    """

    """

    courses = Course.query.all()  # Retrieve all courses from the database
  
    # Logic to fetch admin-related data from the database or other sources
    admin_data = {
        'total_users': 1000,
        'total_orders': 500,
        'new_requests': 10
    }
    # Render the admin dashboard template and pass the admin data to it
    return render_template('admin/admin_dashboard.html', admin_data=admin_data, courses=courses )


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
        return redirect(url_for('admin.register'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin.register'))

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
            return redirect(url_for('admin.register'))
    except Exception as e:
        print(str(e))  # Log the exception for debugging
        db.session.rollback()  # Rollback changes if there's an error
        flash('Error processing file. Please try again.', 'error')

    return redirect(url_for('admin.register'))


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
            course_name = form.course_name.data
            # role = Role.query.filter_by(role='Student').first()
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
            course_obj = Course.query.filter_by(course_name=course_name).first()
            student.class_enrollment = class_obj
            student.course_enrollment = course_obj
            db.session.commit()

            # Send temporary password email
            send_temp_password_email(email, student.student_id, password)

            flash('Student registered successfully!', 'success')
            
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

    # Populate course and class choices for the dropdowns
    form.course_name.choices = [(course.id, course.course_name) for course in Course.query.all()]
    form.class_name.choices = []

    if form.validate_on_submit():


        try:
            username = form.username.data
            email = form.email.data
            password = generate_temp_password()  # Generate temporary password
            class_name = form.class_name.data
            course_name = form.course_name.data

            print("Form Data - Username:", form.username.data, "Email:", form.email.data)
            print(form.validate_on_submit())  # Check if the form is validating correctly
            print(form.errors)  # Print form validation errors  

            # Register teacher
            teacher = Teacher(username=username, email=email, password=password, class_id=class_id, course_id=course_id)
            db.session.add(teacher)
            db.session.commit()

            # Handle class and course relationships
            # Assuming Class and Course models have appropriate relationships defined
            # class_obj = Class.query.filter_by(class_name=class_name).first()
            # course_obj = Course.query.filter_by(course_name=course_name).first()
            # teacher.class_teacher = class_obj
            # teacher.course_teacher = course_obj
            # db.session.commit()

            # Send temporary password email
            # send_temp_password_email(email, teacher.teacher_id, password)

            flash('Teacher registered successfully!', 'success')
            
        except Exception as e:
            print(str(e))  # Log the exception for debugging
            db.session.rollback()  # Rollback changes if there's an error
            flash('Error registering teacher: {}. Please try again'.format(str(e)), 'error')

    return render_template('admin/register_teacher.html', form=form)


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


@admin_bp.route('/register', methods=['GET', 'POST'])
def admin_register():
    """
    Handle the registration of a new student or teacher by the admin.
    Display a registration form for the admin to input user details.
    Register the user in the database and display flash messages for success or error.

    Returns:
        str: A redirect response to the admin dashboard or the registration form page based on form submission.
    """
    student_form = StudentRegistrationForm()
    teacher_form = TeacherRegistrationForm()

    if student_form.validate_on_submit():
        handle_registration(student_form, 'student')

    else:
        handle_registration(teacher_form, 'teacher')

    return render_template('admin/register.html', student_form=student_form, teacher_form=teacher_form)


def handle_registration(form, role):
    try:
        username = form.username.data
        email = form.email.data
        password = generate_temp_password()
        class_name = form.class_name.data
        course_name = form.course_name.data

        print("Form Data - Username:", form.username.data, "Email:", form.email.data)
        print(form.validate_on_submit())  # Check if the form is validating correctly
        print(form.errors)  # Print form validation errors  

        if role == 'student':
            user = Student(username=username, email=email, password=password)
        else:
            user = Teacher(username=username, email=email, password=password)
        
        db.session.add(user)
        db.session.commit()

        # Handle class and course relationships
        class_obj = Class.query.filter_by(class_name=class_name).first()
        course_obj = Course.query.filter_by(course_name=course_name).first()

        if role == 'student':
            user.class_enrollment = class_obj
            user.course_enrollment = course_obj
        else:
            user.class_teacher = class_obj
            user.course_teacher = course_obj

        db.session.commit()

        # Send temporary password email
        send_temp_password_email(email, user.student_id if role == 'student' else user.teacher_id, password)

        flash(f'{role.capitalize()} registered successfully!', 'success')
    except Exception as e:
        print(str(e))  # Log the exception for debugging
        db.session.rollback()  # Rollback changes if there's an error
        flash('Error registering {}: {}. Please try again'.format(role, str(e)), 'error')


@admin_bp.route('/teachers', methods=['GET'])
def display_teachers():
    teachers = Teacher.query.all()  # Query all teachers from the database
    return render_template('admin/teachers.html', teachers=teachers)

@admin_bp.route('/students', methods=['GET'])
def display_students():
    students = Student.query.all()  # Query all students from the database
    return render_template('admin/students.html', students=students)


@admin_bp.route('/get_classes/<int:course_id>')
def get_classes(course_id):
    """
    Endpoint to get classes based on the selected course.
    Returns JSON data containing class information.
    """
    classes = Class.query.filter_by(course_id=course_id).all()
    class_choices = [(cls.id, cls.class_name) for cls in classes]
    return jsonify(class_choices)



@admin_bp.route('/initialize-courses-and-classes')
def initialize_courses_and_classes():
        # List of courses and their associated class names
    courses_data = [
        {
            "course_name": "Mathematics",
            "class_names": ["Math Class A", "Math Class B"]
        },
        {
            "course_name": "Science",
            "class_names": ["Science Class A", "Science Class B"]
        },
        {
            "course_name": "Beauty & Hair",
            "class_names": ["Beauty & Hair Class A", "Beauty & Hair Class B"]
        },
        {
            "course_name": "Graphics",
            "class_names": ["Graphics Class A", "Graphics Class B"]
        },
        {
            "course_name": "Programming",
            "class_names": ["Programming Class A", "Programming Class B"]
        },
        {
            "course_name": "Video Editing",
            "class_names": ["Video Editing Class A", "Video Editing Class B"]
        },
        {
            "course_name": "Camera Operation",
            "class_names": ["Camera Operation Class A", "Camera Operation Class B"]
        },
        {
            "course_name": "Computer Packages",
            "class_names": ["Computer Packages Class A", "Computer Packages Class B"]
        },
        {
            "course_name": "Football",
            "class_names": ["Football Class A", "Football Class B"]
        },
        {
            "course_name": "Taekwondo",
            "class_names": ["Taekwondo Class A", "Taekwondo Class B"]
        },
        {
            "course_name": "Sign Language",
            "class_names": ["Sign Language Class A", "Sign Language Class B"]
        },
        {
            "course_name": "Dance",
            "class_names": ["Dance Class A", "Dance Class B"]
        },
        {
            "course_name": "Korean",
            "class_names": ["Korean Class A", "Korean Class B"]
        },
        {
            "course_name": "Chinese",
            "class_names": ["Chinese Class A", "Chinese Class B"]
        },
        {
            "course_name": "Japanese",
            "class_names": ["Japanese Class A", "Japanese Class B"]
        },
        {
            "course_name": "French",
            "class_names": ["French Class A", "French Class B"]
        },
        {
            "course_name": "Mind Education",
            "class_names": ["Mind Education Class A", "Mind Education Class B"]
        },
        {
            "course_name": "Theology",
            "class_names": ["Theology Class A", "Theology Class B"]
        },
        {
            "course_name": "Music",
            "class_names": ["Music Class A", "Music Class B"]
        }
    ]



    # Initialize courses and classes in the database
    try:
        for course_info in courses_data:
            course_name = course_info["course_name"]
            class_names = course_info["class_names"]
            
            # try:
            #     new_course = Course(course_name=course_name)
            #     db.session.add(new_course)
            #     db.session.commit()
            #     flash("Course created successfully") 

            # except IntegrityError:
            #     db.session.rollback()
            #     existing_course = Course.query.filter_by(course_name=course_name).first()
            #     flash(f"Course '{course_name}' already exists with ID: {existing_course.id}")

           
            existing_course = Course.query.filter_by(course_name=course_name).first()
            
            if existing_course:

                # Course with the same name already exists
                if not existing_course.classes:
                    # If the course has no classes, create classes for it
                    for class_name in class_names:
                        class_obj = Class(class_name=class_name, course=existing_course)
                        db.session.add(class_obj)

                    # Commit the changes for classes related to the current course
                    db.session.commit()
                    flash(f"Classes for '{course_name}' created successfully")

                else:
                    # Course with the same name already exists, you can update it or skip it
                    flash(f"Course '{course_name}' already exists. Skipping...")

                    continue       

            # Create a new course
            new_course = Course(course_name=course_name)
            db.session.add(new_course)
            db.session.commit()
            flash(f"Course '{course_name}' created successfully")

            # Create classes for the course
            for class_name in class_names:
                class_obj = Class(class_name=class_name, course=new_course)
                db.session.add(class_obj)

            # Commit the changes for classes related to the current course
            db.session.commit()

        
    except IntegrityError as e:
        db.session.rollback()
        flash(f"Error: {str(e)}", 'error')
    return redirect(url_for('admin.admin_dashboard'))
                                                                                                                                                                                                                

    flash("Courses and classes initialized successfully.")
    return url_for(admin.admin_dashboard)
