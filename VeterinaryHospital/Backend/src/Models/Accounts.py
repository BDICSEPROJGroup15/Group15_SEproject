from src import db

class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    profile = db.Column(db.LargeBinary(), nullable=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))



    def __repr__(self):
        return '{}'.format(self.username)
