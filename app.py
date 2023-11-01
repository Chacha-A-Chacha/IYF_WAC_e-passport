import os
from app import create_app, db
from flask_migrate import Migrate

# Get the environment from the FLASK_ENV variable; default to 'development' if not set
env = os.environ.get('FLASK_ENV', 'development').lower()

# Create the Flask app using the appropriate configuration class based on the environment
app = create_app(env)

# Initialize Flask-Migrate with the Flask app and the SQLAlchemy database instance
migrate = Migrate(app, db)



if __name__ == '__main__':
    # Run the Flask app
    app.run()


"""
from app import create_app, db  # Import necessary modules from the app package
from flask_migrate import Migrate

# Create the Flask app using the create_app function from the app package
app = create_app()
migrate = Migrate(app, db)

# Use the app context to work within the application
with app.app_context():
    # Apply database migrations
    migrate.init_app(app, db)
    
    # Now you can access parts of your application that require the app context, such as database operations
    # For example, you can create tables if using SQLAlchemy (commented out in this snippet as migrations handle this)
    # db.create_all()  # Avoid creating tables here; use migrations to manage schema changes

if __name__ == '__main__':
    # Run the Flask app
    app.run()

"""