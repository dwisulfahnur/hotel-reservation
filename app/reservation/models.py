import datetime
from app.core.db import db
from app.user.models import User


class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User',
        backref=db.backref('reservation', lazy='dynamic'))
    reservation_code = db.Column(db.String(10))
    checkin_date = db.Column(db.DateTime)
    checkout_date = db.Column(db.DateTime)
    room_number = db.Column(db.Integer)
    room = db.Column(db.Integer)
    adult = db.Column(db.Integer)
    amount = db.Column(db.Float)
    night = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    chekin_status = db.Column(db.Boolean)
    checkout_status = db.Column(db.Boolean)
