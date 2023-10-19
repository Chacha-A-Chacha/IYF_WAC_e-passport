from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FileField, SubmitField
from wtforms.validators import DataRequired, Email


class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth')
    passport_photo = FileField('Passport Photo')
    nationality = StringField('Nationality')
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Phone Number')
    submit = SubmitField('Update Profile')
