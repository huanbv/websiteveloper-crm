import json
from datetime import datetime


from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.orm import relationship

from src import db


class Client(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('client_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(50), nullable=True)
    vat_number = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    zip_code = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('user.email'))
    user = relationship('User', backref='clients')

    client_status_id = db.Column(db.Integer, ForeignKey('client_status.id'))
    client_status = relationship('ClientStatus', backref='clients')

    country_id = db.Column(db.Integer, ForeignKey('country.id'))
    country = relationship('Country', backref='clients')

    currency_id = db.Column(db.Integer, ForeignKey('currency.id'))
    currency = relationship('Currency', backref='clients')


    def __init__(self, name: str, phone: str, email: str, website: str, vat_number: str, address: str, zip_code: str,
                 client_status_id: str, country_id: str, currency_id: str):
        """
        The constructor for Client model.
        :param name: The company's name
        :param phone: The company's phone number
        :param email: The email address of the company
        :param website: The website url address of the company
        :param vat_number: The VAT number of the company
        :param address: The main address of the company
        :param zip_code: The ZIP Code unit
        :param client_status_id: The client status is active or unActive
        :param country_id: The country's company
        :param currency_id: The currency's unit
        """
        self.name = name
        self.phone = phone
        self.email = email
        self.website = website
        self.vat_number = vat_number
        self.address = address
        self.zip_code = zip_code
        self.client_status_id = client_status_id
        self.country_id = country_id
        self.currency_id = currency_id


class ClientStatus(db.Model):
    id = db.Column(db.Integer, Sequence('client_status_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Client Status: {} with {}>'.format(self.id, self.text)


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class ClientOrder(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('client_order_id_seg'), primary_key=True)
    invoice = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    # client_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # orders = db.Column(db.Text)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return '<Client Order: {} with {}>'.format(self.invoice)
