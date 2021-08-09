from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message='Please fill out the email field'),
    ],)

    password = PasswordField(label='Password', validators=[
        DataRequired(message='Please fill out the password field'),
    ],)


