from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    notes = db.relationship('Note')


class Customer(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(150))
    time=db.Column(db.String(150))
    price=db.Column(db.Integer)
    payment=db.Column(db.String(150))
    category=db.Column(db.String(150))
    # date = db.Column(db.String(100), default=datetime.today().strftime('%Y-%m-%d'))

class Student(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(150))
    days=db.Column(db.String(150))
    totalprice=db.Column(db.Integer)
    paidprice=db.Column(db.Integer)
    remainprice = db.Column(db.Integer)
    category = db.Column(db.String(150))
    payment=db.Column(db.String(150))
    course=db.Column(db.String(150))