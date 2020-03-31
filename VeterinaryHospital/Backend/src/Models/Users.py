from src import db
import jwt
from time import time
from flask import current_app

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.Boolean)
    pets= db.relationship('Pet',backref='usr',lazy='dynamic')

    def get_jwt_token(self, expires_in=6000):
        """获取JWT令牌"""
        token=jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
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
