from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired


class ClientForm(FlaskForm):

    inputName = StringField(label='Name', validators=[
        DataRequired(message='Please fill out the name field'),
    ], render_kw={"placeholder": "Client name"})

    inputPhone = StringField(label='Phone Number', validators=[
        DataRequired(message='Please fill out the phone number field'),
    ], render_kw={"placeholder": "Phone number"})

    inputEmail = StringField(label='Email address', validators=[
        DataRequired(message='Please fill out the email address field'),
    ], render_kw={"placeholder": "Email address"})

    inputWebsite = StringField(label='Website', validators=[
        DataRequired(message='Please fill out the website url field'),
    ], render_kw={"placeholder": "Website URL"})

    inputVatNumber = StringField(label='VAT Number', validators=[
        DataRequired(message='Please fill out the VAT number field'),
    ], render_kw={"placeholder": "VAT number"})

    inputAddress = StringField(label='Address', validators=[
        DataRequired(message='Please fill out the address field'),
    ], render_kw={"placeholder": "Address"})

    inputZIPCode = StringField(label='ZIP Code', validators=[
        DataRequired(message='Please fill out the ZIP code field'),
    ], render_kw={"placeholder": "ZIP code"})

    inputClientStatus = SelectField('Client Status', coerce=int)

    inputCountry = SelectField('Country', coerce=int)

    inputCurrency = SelectField('Currency', coerce=int)


class ClientStatusForm(FlaskForm):

    inputText = StringField(label='Status', validators=[
        DataRequired(message='Please fill out the status field'),
    ], render_kw={"placeholder": "Status"})

