from src import db
class staff(db.Model):
    __tablename__='staff'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    def __repr__(self):
        return '{}'.format(self.username)
