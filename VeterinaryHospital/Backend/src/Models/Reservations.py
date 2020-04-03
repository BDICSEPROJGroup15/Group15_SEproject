from src import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__='reservation'
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    staff_id = db.Column(db.Integer,db.ForeignKey('staff.id'),nullable=True)
    pet_id = db.Column(db.Integer,db.ForeignKey('pet.id'),nullable=True)
    type = db.Column(db.Enum('emmergency','standard'))
    place = db.Column(db.Enum('Beijing','Shanghai','Chengdu'))
    state = db.Column(db.Boolean)
    time = db.Column(db.DateTime,default=datetime.now(),nullable=False)

    @staticmethod
    def add_res(staff, pet, type, place, state):
        print("Template: (staff,pet, 'emergency', 'Beijing',true)")
        if type in ['emmergency','stamdard'] and place in ['Beijing','Shanghai','Chengdu'] and isinstance(type,bool):
            reservation = Reservation(id = staff.id, pet=pet.id, type=type, place=place, state=state)
            db.session.add(reservation)
            db.session.commit()
            return reservation
        else:
            return 'Invalid'



    @staticmethod
    def remove_res(id):
        res= Reservation.get_res(id)
        db.session.delete(res)
        db.session.commit()
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
        return ress

    @staticmethod
    def get_res(id=None):
        res = None
        if id is None:
            res=Reservation.query.all().first()
        else:
            res=Reservation.query.filter_by(id = id).first()
        return res




    def __repr__(self):
        return '{}'.format(self.id)
