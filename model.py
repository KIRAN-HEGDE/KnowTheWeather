from datetime import datetime
from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20))
    email = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.String(40), nullable=False)
    latitude = db.Column(db.Float, default=0)
    longitude = db.Column(db.Float, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id