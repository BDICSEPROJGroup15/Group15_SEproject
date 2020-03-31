from src import db

class Pet(db.Model):
    __tablename__='pet'
    id = db.Column(db.Integer, primary_key=True)
    petname=db.Column(db.String(100))
    petage=db.Column(db.String(100))
    petimage=db.Column(db.String(100))
    pettype=db.Column(db.String(100))
    petowner=db.Column(db.Integer, db.ForeignKey('user.id'))

    def create_pet(self, name, age, type, owner):
        pet = Pet(petname=name, petage=age, pettype=type, petowner=owner)
        db.session.add(pet)
        db.session.commit()
        return pet

    def __repr__(self):
        return '{}'.format(self.petname)

