import datetime
from app.core.db import db

class Hotels(db.Model):
    __tablename__ = "Hotels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(30), nullable=False)
    zipcode = db.Column(db.Integer, nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    city = db.relationship('City',
        backref = db.backref('hotels', lazy='dynamic'))
    province_id = db.Column(db.Integer, db.ForeignKey('Province.id'))
    province = db.relationship('Province',
        backref = db.backref('hotels', lazy='dynamic'))
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    country = db.relationship('Country',
        backref = db.backref('hotels', lazy='dynamic'))
    created = db.Column(db.DateTime)

    def __init__(self, name, address, zipcode, city_id, province_id, country_id):
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.city_id = city_id
        self.province_id = province_id
        self.country_id = country_id
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return "<Hotel {}>".format(self.name)

class HotelsFacility(db.Model):
    __tablename__ = "HotelsFacility"
    id = db.Column(db.Integer, primary_key=True)
    hotels_id = db.Column(db.Integer, db.ForeignKey('Hotels.id'))
    hotels = db.relationship('Hotels',
        backref = db.backref('hotels_facility', lazy="dynamic"))
    garage = db.Column(db.Boolean)
    carports = db.Column(db.Boolean)
    swimmingpool = db.Column(db.Boolean)

class City(db.Model):
    __tablename__ = "City"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(30))
    province_id = db.Column(db.Integer, db.ForeignKey('Province.id'))
    province = db.relationship('Province',
        backref = db.backref('city', lazy = 'dynamic'))

    def repr(self):
        return "<City: {}>".format(self.city)

class Province(db.Model):
    __tablename__ = "Province"
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(30))
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    country = db.relationship('Country',
        backref = db.backref('province', lazy='dynamic'))

    def repr(self):
        return "<Province: {}>".format(self.province)

class Country(db.Model):
    __tablename__ = "Country"
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(30))
    code = db.Column(db.String(5))
