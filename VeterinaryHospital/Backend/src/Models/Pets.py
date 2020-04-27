from src.extension import db




class Pet(db.Model):
    __tablename__='pet'
    id = db.Column(db.Integer, primary_key=True)
    petname=db.Column(db.String(100))
    petage=db.Column(db.String(100))
    petimage=db.Column(db.String(100))
    pettype=db.Column(db.String(100))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    reservation = db.relationship("Reservation", backref='pet', lazy='dynamic')


    def __repr__(self):
        return "<Pet '{}'>.".format(self.petname)


    @staticmethod
    def add_pet(name, age, type, owner=None):
        pet = Pet(petname=name, petage=age, pettype=type, petowner=owner.id)
        db.session.add(pet)
        db.session.commit()
        return pet

    @staticmethod
    def remove_pet(id):
        pet= Pet.get_pet(id)
        db.session.delete(pet)
        db.session.commit()
        return pet

        # read method

    @staticmethod
    def read_all(limit=None, order_by=None):
        pets = []
        query = Pet.query
        # if limit is not None:
        #     query=query.limit(limit)
        # if order_by is not None:
        #     query=query.order_by()
        pets = query.all()
        return pets

    @staticmethod
    def get_pet(id=None):
        pet = None
        if id is None:
            pet=Pet.query.first()
        else:
            pet=Pet.query.filter(Pet.id == id).first()
        return pet

    @staticmethod
    def get_user_pet(id=None):
        pet = None
        if id is None:
            # pet=Pet.query.first()
            return None
        else:
            pet=Pet.query.filter(Pet.user_id == id).all()
            # print(pet)
            return pet




    # def __repr__(self):
    #     return '{}'.format(self.petname)

