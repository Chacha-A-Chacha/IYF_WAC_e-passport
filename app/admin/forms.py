#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class TeacherRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    class_name = StringField('Class Name', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired()])
    submit = SubmitField('Register Teacher')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    class_name = StringField('Class Name', validators=[DataRequired()])
    course_name = StringField('Course Name', validators=[DataRequired()])
    additional_info = StringField('Additional Information')  # Add more fields if needed
    submit = SubmitField('Register Student')
