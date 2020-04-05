from src import db

class Message(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.String(128),index=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))




    def __repr__(self):
        return '<Message {}>'.format(self.content)