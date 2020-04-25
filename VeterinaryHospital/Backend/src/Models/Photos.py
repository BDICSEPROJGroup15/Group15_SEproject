from datetime import datetime
from src import db

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    photos=db.relationship('Photo',bacl_populates='author',cascade='all')

class Photo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(500))
    filename=db.Column(db.String(64))
    timestap=db.Column(db.DateTime,default=datetime.utcnow())
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',back_populates='photo')