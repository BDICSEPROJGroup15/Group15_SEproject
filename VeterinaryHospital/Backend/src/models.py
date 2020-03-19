from datetime import datetime
from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean)
    pet = db.relationship('Pet',backref='pet',lazy='dynamic')
    
    def __repr__(self):
        return '{}'.format(self.username)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '{}'.format(self.username)

class Pet(db.Model):
	__tablename__='pet'
	id = db.Column(db.Integer, primary_key=True)
	petname=db.Column(db.String(100))
	petage=db.Column(db.String(100))
	petimage=db.Column(db.String(100))
	pettype=db.Column(db.String(100))
	petowner=db.Column(db.Integer, db.ForeignKey('user.id'))


# class Profile(db.Model):

# class Reservation(db.Model):

