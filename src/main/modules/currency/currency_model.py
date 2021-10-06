from sqlalchemy import Sequence

from src import db


class Currency(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, Sequence('currency_id_seg'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)

    def __init__(self, name: str, symbol: str):
        """
        The constructor for Currency model.
        :param name: The currency's currency
        :param symbol: The symbol's currency
        """
        self.name = name
        self.symbol = symbol
