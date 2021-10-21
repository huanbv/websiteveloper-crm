import json
from datetime import datetime


from sqlalchemy import ForeignKey, Sequence, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from src import db


class Invoice(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('invoice_id_seg'), primary_key=True)
    invoice = db.Column(db.String(50), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    payment_status_id = db.Column(db.Integer, ForeignKey('payment_status.id'))
    payment_status = relationship('PaymentStatus', backref='invoices')

    delivery_status_id = db.Column(db.Integer, ForeignKey('delivery_status.id'))
    delivery_status = relationship('DeliveryStatus', backref='invoices')

    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    client = relationship('Client', backref='invoices')

    currency_id = db.Column(db.Integer, ForeignKey('currency.id'))
    currency = relationship('Currency', backref='invoices')

    def __repr__(self):
        return '<Invoice %r>' % self.invoice


    def get_status_class(self):
        if self.client_status_id == 1:
            return "border border-green-500 text-green-700"
        else:
            return "border border-red-500 text-red-700"


class PaymentStatus(db.Model):
    id = db.Column(db.Integer, Sequence('payment_status_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Invoice payment Status: {} with {}>'.format(self.id, self.text)


class DeliveryStatus(db.Model):
    id = db.Column(db.Integer, Sequence('delivery_status_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Invoice delivery Status: {} with {}>'.format(self.id, self.text)


class InvoiceItem(db.Model):
    invoice_id = db.Column(db.Integer, ForeignKey('invoice.id'))
    invoice = relationship('Invoice', backref=db.backref('invoice_items',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    product = relationship('Product', backref=db.backref('invoice_items',
                                        cascade="save-update, merge, "
                                                "delete, delete-orphan"))

    __table_args__ = (
        PrimaryKeyConstraint(invoice_id, product_id),
    )
