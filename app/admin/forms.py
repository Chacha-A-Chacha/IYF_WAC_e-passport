#!/usr/bin/env python3
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email

class TeacherRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course_name = SelectField('Select Course', validators=[DataRequired()], coerce=int)
    class_name = SelectField('Select Class', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Register Teacher')

class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    course_name = SelectField('Select Course', validators=[DataRequired()], coerce=int)
    class_name = SelectField('Select Class', validators=[DataRequired()], coerce=int)
    additional_info = StringField('Additional Information')
    submit = SubmitField('Register Student')
