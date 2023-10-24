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

    # Register blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .admin import admin_bp as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .teacher import teacher_bp as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')

    return app
