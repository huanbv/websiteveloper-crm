from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class SignupForm(FlaskForm):
    email = StringField(label='Email', validators=[
        DataRequired(message='Please fill out the email field'),
    ],)

