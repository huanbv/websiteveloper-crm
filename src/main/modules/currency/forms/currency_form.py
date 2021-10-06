from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CurrencyForm(FlaskForm):

    inputName = StringField(label='Name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Name"})

    inputSymbol = StringField(label='Symbol', validators=[
        DataRequired(message='Please fill out the symbol field'),
    ], render_kw={"placeholder": "Symbol"})

