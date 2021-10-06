from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired


class ContactForm(FlaskForm):

    inputFirstName = StringField(label='First name', validators=[
        DataRequired(message='Please fill out the first name field'),
    ], render_kw={"placeholder": "First name"})

    inputMiddleName = StringField(label='Middle name', validators=[
        DataRequired(message='Please fill out the middle name field'),
    ], render_kw={"placeholder": "Middle name"})

    inputLastName = StringField(label='Last name', validators=[
        DataRequired(message='Please fill out the last name field'),
    ], render_kw={"placeholder": "Last name"})

    inputPosition = StringField(label='Position', validators=[
        DataRequired(message='Please fill out the position field'),
    ], render_kw={"placeholder": "Position"})

    inputEmail = StringField(label='Email address', validators=[
        DataRequired(message='Please fill out the Email address field'),
    ], render_kw={"placeholder": "Email address"})

    inputPhone = StringField(label='Phone number', validators=[
        DataRequired(message='Please fill out the phone number field'),
    ], render_kw={"placeholder": "Phone number"})

    inputDOB = DateTimeLocalField('Date of Birth', format='%Y-%m-%dT%H:%M', validators=[DataRequired(
        message="Please enter your date of birth!")])

    inputAlternateContactNumber = StringField('Alternate contact number', validators=[DataRequired(
        message="Please enter your Alternate contact number!")])

    inputGender = SelectField('Gender', coerce=int)

    inputClient = SelectField('Client', coerce=int)
