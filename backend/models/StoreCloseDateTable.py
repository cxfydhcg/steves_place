"""Database model for order persistence in Steve's Place.

This module defines the StoreClosedDate class which represents the database
schema for storing store closed dates with SQLAlchemy ORM.
"""

from flask_sqlalchemy import SQLAlchemy
from db import db

class StoreClosedDateTable(db.Model):
    """
    Represents a closed date for a store.

    This model stores information about dates when a store is closed,
    including one-time closures and recurring closures on specific weekdays.

    Attributes:
        id (int): Primary key for the table.
        date (date): Specific date when the store is closed.
        is_recurring (bool): True if the closure is recurring, False otherwise.
    """
    __tablename__ = 'store_closed_dates'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    is_recurring = db.Column(db.Boolean, nullable=False, default=False)
    
    def __init__(self, date, is_recurring=False):
        # and duplicate date can not be created
        if self.query.filter_by(date=date).first():
            raise Exception("Duplicate date can not be created")
            
        self.date = date
        self.is_recurring = is_recurring
    @classmethod
    def is_closed_on(cls, date):
        if cls.query.filter_by(date=date).first():
            return True
        if cls.query.filter_by(is_recurring=True).first():
            return True
        if date.weekday() == 6:
            return True
        return False
        
