from src import db




class Pet(db.Model):
    __tablename__='pet'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    petname=db.Column(db.String(100))
    petage=db.Column(db.String(100))
    petimage=db.Column(db.String(100))
    pettype=db.Column(db.String(100))
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))
    reservation = db.relationship("Reservation", backref='pet', lazy='dynamic')


    def __repr__(self):
        return "<Pet '{}'>.".format(self.petname)


    @staticmethod
    def add_pet(name, age, image, type, user):
        print("add a pet: [petname: %s, petage: %s, petimage: %s, pettype: %s]" % (name, age, image, type))
        pet = Pet(petname=name, petage=age, petimage=image, pettype=type, user=user)
        db.session.add(pet)
        db.session.commit()
        print("add reservation successfully")
        return pet

    @staticmethod
    def remove_pet(id):
        pet= Pet.get_pet(id)
        if pet != None:
            db.session.delete(pet)
            db.session.commit()
            print("remove pet successfully")
            return pet
        else:
            print("wrong pet remove")

        # read method

    @staticmethod
    def read_all(limit=None, order_by=None):
        query = Pet.query
        # if limit is not None:
        #     query=query.limit(limit)
        # if order_by is not None:
        #     query=query.order_by()
        pets = query.all()
        print("read all pets successfully")
        return pets

    @staticmethod
    def get_pet(id=None):
        id=int(id)
        if id is None:
            return None
        else:
            pet=Pet.query.filter(Pet.id == id).first()
            print("get pet id: " + str(id))
            print("pet id: " + str(pet.id))
            if pet.id == id:
                print("yes")
                return pet
            else:
                return None

