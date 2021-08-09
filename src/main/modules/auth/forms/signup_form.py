from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


class SignupForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message='Please fill out the email field'),
    ],)

    first_name = StringField(label='First name', validators=[
        Length(max=30, message='Maximum 30 letters'),
        DataRequired(message='Please fill out the first name field')
    ])

    last_name = StringField(label='First name', validators=[
        Length(max=20, message='Maximum 20 letters'),
        DataRequired(message='Please fill out the first name field')
    ])

    password = PasswordField(label='Password', validators=[
        DataRequired(message='Please fill out the password field')
    ])

    re_password = PasswordField(label='Re-enter the password', validators=[
        EqualTo('password', message='The password do not match'),
        DataRequired(message='Please fill out all the password fields')
    ])

