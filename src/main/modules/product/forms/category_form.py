from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProductCategoryForm(FlaskForm):

    inputName = StringField(label='Product category name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Product category name"})


