import jwt
from src import db
from time import time
from src.Models.Pets import Pet
from flask import current_app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=False)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean)

    pets = db.relationship('Pet',
                           backref='user',
                           lazy='dynamic')
    reservations = db.relationship('Reservation', backref='user',
                                   lazy='dynamic')


    @staticmethod
    def get_user(id):
        user = User.query.filter(User.id == id).first()
        return user

    @staticmethod
    def read_all():
        return User.query.all()

    # add a new Pet
    def add_pet(self, pet):
        if isinstance(pet, Pet):
            pet.user_id = self.id
        else:
            raise Exception()
        db.session.add(pet)
        db.session.commit()

    def get_jwt_token(self, expires_in=6000):
        """get JWT token"""
        token = jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                           current_app.config['SECRET_KEY'],
                           algorithm='HS256').decode('utf8')

        print(token)
        return token

    @staticmethod
    def verify_jwt_token(token):
        try:
            user_id = jwt.decode(token,
                                 current_app.config['SECRET_KEY'],
                                 algorithms='HS256')['reset_password']
        except Exception as e:
            print(e)
            return
        return User.query.get(user_id)


    def __repr__(self):
        return '{}'.format(self.username)


