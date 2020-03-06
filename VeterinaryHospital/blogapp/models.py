from datetime import datetime
from blogapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean)

    def __repr__(self):
        return '{}'.format(self.username)


# class Pet(db.Model):

# class Profile(db.Model):

# class Reservation(db.Model):

