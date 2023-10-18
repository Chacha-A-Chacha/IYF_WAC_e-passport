#!/src/bin/env python3

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string_as_your-secret-key'
    # Change this to your preferred database URL
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Flask-Mail Configuration (if using email)
    # MAIL_SERVER = 'smtp.example.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    # MAIL_USERNAME = 'your-email@example.com'
    # MAIL_PASSWORD = 'your-email-password'

    # Flask-Assets Configuration
    # ASSETS_DEBUG = True  # Set to True during development for debugging
    # ASSETS_AUTO_BUILD = True  # Set to True during development for automatic asset building

    # Tailwind CSS Configuration
    # TAILWIND_CSS = {
    #     'output_path': 'gen/static/css/',
    #     'entry_file': 'static/src/input.css',  # Path to your main Tailwind CSS file
    # }

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
    "development": DevelopmentConfig,
    "default": DevelopmentConfig
}
