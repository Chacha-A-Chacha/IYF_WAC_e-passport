from app import create_app, db, models
# from flask_script import Manager
from flask_migrate import Migrate  # upgrade

# Create the Flask app using the create_app function from the app package
app = create_app()
migrate = Migrate(app, db)
# manager = Manager(app)


# Use the app context to work within the application
with app.app_context():
    # Now you can access parts of your application that require the app context, such as database operations
    # For example, you can create tables if using SQLAlchemy
    db.create_all()

if __name__ == '__main__':
    # Run the Flask app
    app.run()
