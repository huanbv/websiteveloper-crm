from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class SignupForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message='Please fill out the email field'), Email(),
    ], render_kw={"placeholder": "Email"})

    first_name = StringField(label='First name', validators=[
        Length(max=30, message='Maximum 30 letters'),
        DataRequired(message='Please fill out the first name field')
    ], render_kw={"placeholder": "First Name"})

    last_name = StringField(label='Last name', validators=[
        Length(max=20, message='Maximum 20 letters'),
        DataRequired(message='Please fill out the first name field')
    ], render_kw={"placeholder": "Last Name"})

    password = PasswordField(label='Password', validators=[
        DataRequired(message='Please fill out the password field')
    ], render_kw={"placeholder": "Password"})

    re_password = PasswordField(label='Re-enter the password', validators=[
        EqualTo('password', message='The password do not match'),
        DataRequired(message='Please fill out all the password fields')
    ], render_kw={"placeholder": "Re-Enter The Password"})

