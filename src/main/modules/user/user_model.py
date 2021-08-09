from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from src import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)


    def __init__(self, first_name: str, last_name: str, raw_password: str):
        """
        The constructor for User model.
        :param first_name: The user's first name (included middle name)
        :param last_name: The user's lastname
        :param raw_password: The raw password string of the user
        """
        self.first_name = first_name
        self.last_name = last_name
        self.password_hash = self.get_hash_password(raw_password)


    def get_id(self):
        """
        Overriding the function of flask_login
        :return: the id ofd current user
        """
        return self.id


    def get_hash_password(self, raw_password: str):
        """
        Generating a hashed string from the raw_password.
        :param raw_password: The raw password string of the user
        :return: Hashed password string
        """
        assert(str is not None, 'The raw_password cannot be None.')
        return generate_password_hash(self.password)

