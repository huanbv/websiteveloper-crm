from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message='Please fill out the email field'), Email(),
    ], render_kw={"placeholder": "Email or Username"})

    password = PasswordField(label='Password', validators=[
        DataRequired(message='Please fill out the password field'),
    ], render_kw={"placeholder": "Password"})


