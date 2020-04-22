from src import db
from datetime import datetime


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # username = db.Column(db.String, nullable=True)
    # petname = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=True)
    state = db.Column(db.String, nullable=True)
    place = db.Column(db.String, nullable=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'))
    @staticmethod
    def add_res(user, pet, type, state, place):
        print("save reservation: [username: %s, petname: %s, type: %s, state: %s, place: %s]" % (
        user.username, pet.petname, type, place, state))
        if type in ['emergency', 'standard'] and place in ['Beijing', 'Shanghai', 'Chengdu'] and state in ['surgery confirmed', 'completed', 'ready for release']:
            reservation = Reservation(user=user, pet=pet, type=type, place=place, state=state)
            db.session.add(reservation)
            db.session.commit()
            print("add reservation successfully")
            return reservation
        else:
            return 'Invalid'

    @staticmethod
    def remove_res(id):
        res = Reservation.get_res(id)
        db.session.delete(res)
        db.session.commit()
        print("remove reservation successfully")
        return res

        # read method

    @staticmethod
    def read_all(limit=None, order_by=None):
        query = Reservation.query
        # if limit is not None:
        #     query=query.limit(limit)
        # if order_by is not None:
        #     query=query.order_by()
        ress = query.all()
        print("read all reservation successfully")
        return ress

    @staticmethod
    def get_res(id=None):
        if id is None:
            res = Reservation.query.first()
        else:
            res = Reservation.query.filter(id == id).first()
            print("get reservation id: "+id)
        return res

    def __repr__(self):
        return '{}'.format(self.id)
