from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import db
from app.auth import auth_bp
from app.models import User
from app.auth.forms import RegistrationForm, LoginForm


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data)
        user.set_password(form.password.data)  # Set hashed password
        db.session.add(user)  # add the new user to our database session (in memory only for now)
        db.session.commit()  # commit all changes in this transaction so they are saved into the DB!

        flash('Congratulations, you are now a registered user!', 'success')
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', title='Register', form=form)

    # end of function


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Login successful!', 'success')

            # Redirect users based on their roles
            if user.role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            elif user.role == 'teacher':
                return redirect(url_for('teacher.dashboard'))
            elif user.role == 'student':
                return redirect(url_for('student.dashboard'))
            else:
                return redirect(url_for('admin.admin_dashboard'))  # Redirect to a default dashboard if role is undefined

        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html', title="Sign In", form=form)


@auth_bp.route('/logout')
def logout():
    # remove the token from the cookie and log out the user
    # we do it by setting the expiration date to sometime in the past
    # resp= make_response(redirect(url_for("main.index")))
    logout_user()
    return redirect(url_for('main.index'))
