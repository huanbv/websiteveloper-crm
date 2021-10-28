from flask_wtf import FlaskForm
from wtforms import SelectField

from src.main.modules.invoice.fields.item_field import ItemField



class InvoiceForm(FlaskForm):

    items = ItemField()

    # inputProductName = StringField(label='Product Name', validators=[
    #     DataRequired(message='Please fill out the product name field'),
    # ], render_kw={"placeholder": "Product name"})
    #
    # inputProductPrice = StringField(label='Product Price', validators=[
    #     DataRequired(message='Please fill out the product price field'),
    # ], render_kw={"placeholder": "Product Price"})
    #
    # inputProductDiscount = StringField(label='Discount', validators=[
    #     DataRequired(message='Please fill out the discount field'),
    # ], render_kw={"placeholder": "Discount"})
    #
    # inputProductQuantity = StringField(label='Quantity', validators=[
    #     DataRequired(message='Please fill out the product quantity field'),
    # ], render_kw={"placeholder": "Quantity"})
    #
    # inputProductColor = StringField(label='Color', validators=[
    #     DataRequired(message='Please fill out the color field'),
    # ], render_kw={"placeholder": "Color"})
    #
    # inputProductDescription = StringField(label='Description', validators=[
    #     DataRequired(message='Please fill out the description field'),
    # ], render_kw={"placeholder": "Description"})

    inputPaymentStatus = SelectField('Payment Status', coerce=int)

    inputDeliveryStatus = SelectField('Delivery Status', coerce=int)

    inputClient = SelectField('Client', coerce=int)

    inputCurrency = SelectField('Currency', coerce=int)


