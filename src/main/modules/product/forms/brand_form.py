from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProductBrandForm(FlaskForm):

    inputName = StringField(label='Product brand name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Product brand name"})


