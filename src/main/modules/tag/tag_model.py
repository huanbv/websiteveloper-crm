from sqlalchemy import Sequence

from src import db


class Tag(db.Model):
    id = db.Column(db.Integer, Sequence('tag_id_seq'), primary_key=True)
    name = db.Column(db.String(25), unique=True)
