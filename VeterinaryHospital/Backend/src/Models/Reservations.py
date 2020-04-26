from src.extension import db
from datetime import datetime


class Reservation(db.Model):
    __tablename__ = 'reservation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = ""
    petname = ""
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
        if type in ['emergency', 'standard'] and place in ['Beijing', 'Shanghai', 'Chengdu'] and state in [
            'surgery confirmed', 'completed', 'ready for release']:
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
        if res != None:
            db.session.delete(res)
            db.session.commit()
            print("remove reservation successfully")
            return res
        else:
            print("wrong reservation remove")
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
        id=int(id)
        if id is None:
            # res = Reservation.query.first()
            return None
        else:
            res = Reservation.query.filter(Reservation.id == id).first()
            print("get reservation id: " + str(id))
            print("reservation id: " + str(res.id))
            if res.id == id:
                print("11")
                return res
            else:
                return None

    @staticmethod
    def set_user_pet_name(reservation=None, user=None, pet=None):
        if reservation is not None:
            if user is not None:
                reservation.username = user.username
            if pet is not None:
                reservation.petname = pet.petname
        # print(reservation)
        return reservation

    @staticmethod
    def update_state(list=None):
        if list is None:
            return
        else:
            print("update state")
            res = Reservation.query.filter(Reservation.id == int(list[0])).first()
            res.state=list[1]
            print(res)
            db.session.commit()
    def __repr__(self):
        return '<id: {},type: {},state: {},place: {},timestamp: {},user_id: {},pet_id: {}>'.format(self.id, self.type,
                                                                                                   self.state,
                                                                                                   self.place,
                                                                                                   self.timestamp,
                                                                                                   self.user_id,
                                                                                                   self.pet_id)
