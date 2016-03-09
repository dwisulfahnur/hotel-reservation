import datetime
from app.core.db import db
from flask.ext.bcrypt import generate_password_hash
from flask.ext.login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    fullname = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(30), nullable=False, unique=True)
    address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    def __init__(self, fullname, username, email, address, phone_number, password):
        self.fullname = fullname
        self.username = username
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.password = generate_password_hash(password)
        self.created = datetime.datetime.now()

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def get_id(self):
        return unicode(self.id)
    def is_anonymous(self):
        return False

    def __repr__(self):
        return "<Username: %s>"%self.username

class Roles(db.Model):
    __tablename__ = "Roles"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    description = db.Column(db.String(50), nullable=False)

class UserRoles(db.Model):
    __tablename__ = "UserRoles"
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("Roles.id"))
    role = db.relationship('Roles',
        backref = db.backref('user_roles', lazy='dynamic'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User',
        backref = db.backref('user_roles', lazy='dynamic'))

    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id

    def __repr__(self):
        return "<User %s as %s"%(self.user_id,self.role_id)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    user = db.relationship('User',
        backref = db.backref('profile', lazy='dynamic'))
    birthdate = db.Column(db.DateTime, nullable=False)
    birthplace = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.Boolean, nullable=False)
