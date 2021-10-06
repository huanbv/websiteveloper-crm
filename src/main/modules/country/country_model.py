from sqlalchemy import Sequence

from src import db


class Country(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('country_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name: str):
        """
        The constructor for country model.
        :param name: The name's country
        """
        self.name = name


class State(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    country_id = db.Column(db.Integer)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    state_id = db.Column(db.Integer)
