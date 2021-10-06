from sqlalchemy import ForeignKey, Sequence
from sqlalchemy.orm import relationship

from src import db


class Contact(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('contact_id_seg'), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    middle_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    alternate_contact_number = db.Column(db.String(50), nullable=True)

    user_id = db.Column(db.Integer, ForeignKey('user.email'))
    user = relationship('User', backref='contacts')

    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    client = relationship('Client', backref='contacts')

    gender_id = db.Column(db.Integer, ForeignKey('gender.id'))
    gender = relationship('Gender', backref='contacts')


    def __init__(self, first_name: str, middle_name: str, last_name: str, position: str, email: str, phone: str,
                 dob: str, alternate_contact_number: str, client_id: str, gender_id: str):
        """
        The constructor for Client model.
        :param first_name: The first name's contact
        :param middle_name: The middle name's contact
        :param last_name: The last name's contact
        :param position: The position's contact
        :param email: The email's contact
        :param phone: The phone's contact
        :param dob: The date of birth's contact
        :param alternate_contact_number: The alternate contact number's contact
        :param client_id: The main company's contact
        :param gender_id: The gender's contact
        """
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.position = position
        self.email = email
        self.phone = phone
        self.dob = dob
        self.alternate_contact_number = alternate_contact_number
        self.client_id = client_id
        self.gender_id = gender_id


class Gender(db.Model):
    id = db.Column(db.Integer, Sequence('gender_id_seq'), primary_key=True)
    text = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Gender: {} with {}>'.format(self.id, self.text)
