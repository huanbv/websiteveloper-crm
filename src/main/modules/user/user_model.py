from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from src import db


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}

    email = db.Column(db.String(100), nullable=False, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


    def __init__(self, email: str, first_name: str, last_name: str, raw_password: str):
        """
        The constructor for User model.
        :param first_name: The user's first name (included middle name)
        :param last_name: The user's lastname
        :param raw_password: The raw password string of the user
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.get_hash_password(raw_password)


    def get_id(self):
        """
        Overriding the function of flask_login
        :return: the id ofd current user
        """
        return self.email


    def get_hash_password(self, raw_password: str):
        """
        Generating a hashed string from the raw_password.
        :param raw_password: The raw password string of the user
        :return: Hashed password string
        """
        assert(str is not None, 'The raw_password cannot be None.')
        return generate_password_hash(raw_password)


    def check_password_hash(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


class UserRole(db.Model):
    user_email = db.Column(db.String(100), ForeignKey('user.email'), primary_key=True)
    user = relationship('User', backref='roles')

    role_id = db.Column(db.Integer, ForeignKey('role.id'), primary_key=True)
    role = relationship('Role', backref='items')

