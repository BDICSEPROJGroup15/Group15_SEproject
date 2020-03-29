# controllers.py
#
from src import db
from src.models import Pet
from sqlalchemy import desc

class controllers():
    def create_pet(self, name, age,  type, owner):
        pet = Pet(petname = name, petage =age, pettype=type, petowner=owner)
        db.session.add(pet)
        db.session.commit()

        return pet
