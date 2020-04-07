from src import db

class Staff(db.Model):

    __tablename__='staff'
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))


    @staticmethod
    def create(username="", password=""):
        staff =  Staff(username=username,password_hash=password)
        db.session.add(staff)
        db.session.commit()


    # read method
    @staticmethod
    def read_all(limit=None, order_by=None):
        staffs = []
        query=Staff.query
        # if limit is not None:
        #     query=query.limit(limit)
        # if order_by is not None:
        #     query=query.order_by()
        staffs=query.all()
        return staffs


    # conditional query



    #Update methods



    #Delete methods
