from sqlalchemy import Sequence, ForeignKey
from sqlalchemy.orm import relationship

from src import db

from datetime import datetime


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Integer, default=0)
    stock = db.Column(db.Integer, nullable=False)
    colors = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product_brand_id = db.Column(db.Integer, ForeignKey('product_brand.id'))
    product_brand = relationship('ProductBrand', backref='products')

    product_category_id = db.Column(db.Integer, ForeignKey('product_category.id'))
    product_category = relationship('ProductCategory', backref='products')

    thumbnail = db.Column(db.String(150), nullable=False, default='image.jpg')

    def __repr__(self):
        return '<Product %r>' % self.name


class ProductBrand(db.Model):
    id = db.Column(db.Integer, Sequence('product_brand_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Product brand: {} with {}>'.format(self.id, self.text)


class ProductCategory(db.Model):
    id = db.Column(db.Integer, Sequence('product_category_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Product category: {} with {}>'.format(self.id, self.text)
