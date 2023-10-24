#!/src/bin/env python3

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Base configuration class for the Flask application.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string_as_your-secret-key'
    # Change this to your preferred database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Flask-Mail Configuration (if using email)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your-email@gmail.com'  # Your Gmail email address
    MAIL_PASSWORD = 'your-gmail-password-or-app-password'  # Your Gmail password or App Password

    @staticmethod
    def init_app(app):
        """
        Initialize the Flask application with this configuration.

        Parameters:
            app (Flask): The Flask application instance.

        Returns:
            None
        """
        pass

class DevelopmentConfig(Config):
    """
    Configuration class for development environment.
    """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
