from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import IntegerField, StringField, TextAreaField

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):

    inputName = StringField(
        label='Name',
        validators=[
            DataRequired(message='Please fill out the name field'),
        ],
        render_kw={"placeholder": "Product title"},
    )

    inputPrice = IntegerField(
        label='Price',
        validators=[
            DataRequired(message='Please fill out the price field'),
        ],
        render_kw={"placeholder": "Product price"},
    )

    inputDiscount = IntegerField(
        label='Discount',
        validators=[
            DataRequired(message='Please fill out the discount field'),
        ], render_kw={"placeholder": "Product discount"},
        default=0,
    )

    inputStock = IntegerField(
        label='Stock',
        validators=[
            DataRequired(message='Please fill out the stock field'),
        ],
        render_kw={"placeholder": "Product in-stock"},
    )

    inputDescription = TextAreaField(
        label='Description',
        validators=[
            DataRequired(message='Please fill out the description field'),
        ],
        render_kw={"placeholder": "Product description"},
    )

    inputColor = TextAreaField(
        label='Colors',
        validators=[
            DataRequired(message='Please fill out the color field'),
        ],
        render_kw={"placeholder": "Product color"},
    )

    inputThumbnail = FileField(
        label='Thumbnail image',
        render_kw={'accept': 'image/png, image/jpeg, image/jpg'},
        validators=[
            FileAllowed(
                upload_set=['png', 'jpg', 'jpeg'],
                message='Only png or jpg or jpeg image allowed'
            ),
        ]
    )
