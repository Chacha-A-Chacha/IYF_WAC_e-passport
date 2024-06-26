import string
import secrets
from flask_mail import Message  # This class represents an email message.
from flask import current_app  # Flask's way of referring to the current application context.

from app import mail


def generate_temp_password(length=12):
    """
    Generate a temporary password with the specified length.

    Parameters:
    - length (int): Length of the generated password. Default is 12 characters.

    Returns:
    - str: Generated temporary password.
    """
    characters = string.ascii_letters + string.digits + string.punctuation
    temp_password = ''.join(secrets.choice(characters) for _ in range(length))
    return temp_password

    # Example usage
    # temp_password = generate_temp_password()
    # print(temp_password)


def send_temp_password_email(email, temp_password):
    """
    Sends an email with the temporary password to the specified email address.

    Parameters:
        email (str): The recipient's email address.
        temp_password (str): The temporary password to be sent in the email.

    Returns:
        None

    Raises:
        Any exceptions raised during the email sending process.

    Example:
        send_temp_password_email('user@example.com', 'temp_password123')
    """
    try:
        # Create a message object
        msg = Message('Temporary Password', sender=current_app.config['MAIL_USERNAME'], recipients=[email])

        # Compose the email body
        msg.body = f'Your temporary password is: {temp_password}. Please reset your password after logging in.'

        # Send the email
        current_app.mail.send(msg)

        # Optionally, handle successful email sending (e.g., log the event)
        # logger.info(f'Temporary password email sent to {email}')

    except Exception as e:
        # Handle exceptions raised during the email sending process
        # logger.error(f'Error sending temporary password email to {email}: {str(e)}')
        raise e







from flask_login import login_required, current_user

# Custom decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash("Unauthorized. Admins only!", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Custom decorator for teacher-only routes
def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'teacher':
            flash("Unauthorized. Teachers only!", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
