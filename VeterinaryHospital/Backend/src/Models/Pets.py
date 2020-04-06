from src import db




class Pet(db.Model):
    __tablename__='pet'
    id = db.Column(db.Integer, primary_key=True)
    petname=db.Column(db.String(100))
    petage=db.Column(db.String(100))
    petimage=db.Column(db.String(100))
    pettype=db.Column(db.String(100))
    petowner=db.Column(db.Integer, db.ForeignKey('user.id'))



    @staticmethod
    def add_pet(name, age, type, owner=None):
        pet = Pet(petname=name, petage=age, pettype=type, petowner=owner)
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
            pet=Pet.query.all().first()
        else:
            pet=Pet.query.filter_by(id = id).first()
        return pet





    # def __repr__(self):
    #     return '{}'.format(self.petname)

