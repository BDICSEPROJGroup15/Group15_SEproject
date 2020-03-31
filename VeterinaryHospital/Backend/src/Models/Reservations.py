from src import db


class Reservation(db.Model):
    __tablename__='reservation'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=True)
    pet_id = db.Column(db.Integer,db.ForeignKey('pet.id'),nullable=True)
    type = db.Column(db.Enum('emmergency','standard'))
    place = db.Column(db.Enum('Beijing','Shanghai','Chengdu'))
    state = db.Column(db.Boolean)
    time = db.Column(db.Time)

    def __repr__(self):
        return '{}'.format(self.id)
