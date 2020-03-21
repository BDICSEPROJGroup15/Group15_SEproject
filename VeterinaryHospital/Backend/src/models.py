from datetime import datetime
from src import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean)
    pets= db.relationship('Pet',backref='usr',lazy='dynamic')
    
    def __repr__(self):
        return '{}'.format(self.username)

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    profile = db.Column(db.LargeBinary(), nullable=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))



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


    def __repr__(self):
        return '{}'.format(self.petname)


class staff(db.Model):
    __tablename__='staff'
    staff_id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '{}'.format(self.username)

# class Profile(db.Model):

class Reservation(db.Model):
    __tablename__='reservation'
    id = db.Column(db.Integer,primaryKey=True, autoincrement=True)
    staff_id = db.Column(db.Integer,db.Foreignkey('staff.id'),nullable=True)
    pet_id = db.Column(db.Integer,db.ForeignKey('pet.id'),nullable=True)
    type = db.Column(db.Enum('emmergency','standard'))
    place = db.Column(db.Enum('Beijing','Shanghai','Chengdu'))
    state = db.Column(db.Boolean)
    time = db.Column(db.Time)

    def __repr__(self):
        return '{}'.format(self.id)


class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.String(128),index=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Message {}>'.format(self.content)