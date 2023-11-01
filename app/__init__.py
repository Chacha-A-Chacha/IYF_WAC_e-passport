from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail

from config import config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()

def create_app(env='development'):
    """
    Creates and configures the Flask application.

    Parameters:
        env (str): The environment for which the application is configured. Default is 'development'.

    Returns:
        Flask: The configured Flask application instance.

    The create_app function initializes and configures the Flask application by loading the appropriate
    configuration based on the specified environment. It sets up extensions such as SQLAlchemy, Flask-Migrate,
    Flask-Login, Flask-Bcrypt, and Flask-Mail. Blueprints for different parts of the application (main, authentication,
    admin, teacher) are registered here, allowing for modular and organized project structure.

    Example Usage:
        To create an application for the development environment:
        >>> app = create_app(env='development')

        To create an application for the production environment:
        >>> app = create_app(env='production')
    """
    app = Flask(__name__)

    # Select appropriate configuration based on the environment
    app.config.from_object(config.get(env, config['development']))
    config[env].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Specify the login view for authentication

    @app.cli.command()
    def init_courses_and_classes():
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
        for course_info in courses_data:
            course_name = course_info["course_name"]
            class_names = course_info["class_names"]
            
            # Create the course
            course = Course(course_name=course_name)
            db.session.add(course)
            db.session.commit()  # Commit course to get the course ID
            
            # Create classes for the course
            for class_name in class_names:
                class_obj = Class(class_name=class_name, course=course)
                db.session.add(class_obj)

            # Commit the changes for classes related to the current course
            db.session.commit()

        # Commit the final changes to the database
        db.session.commit()
                                                                                                                                                                                                                    

        print("Courses and classes initialized successfully.")


    # Register blueprints
    from .student import student_bp as student_blueprint
    app.register_blueprint(student_blueprint)

    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin_bp as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .teacher import teacher_bp as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    return app
