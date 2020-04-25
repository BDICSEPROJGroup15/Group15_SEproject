from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm, AddReservation, EditReservation, \
    AddReservationForm
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Models.Users import User
from flask import render_template, flash, redirect, url_for, session, request, jsonify, abort, make_response,Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from src import app, db
from src.Models.Pets import Pet
from src.Models.Reservations import Reservation
from config import Config
import os
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Controllers.reservation import reservation
pets = Blueprint('pets', __name__, template_folder="/template/pets",
                        static_folder='static/uploaded_PH', url_prefix='/pets')

@pets.route('/')
@pets.route('/index',methods=['GET','POST'])
def index():
    form = PetForm()
    if not session.get("USERNAME") is None:
        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        if form.validate_on_submit():
            pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
            ph_dir = Config.PH_UPLOAD_DIR
            file_obj = form.petimage.data
            ph_filename = form.petname.data + '_PPH.jpg'
            file_obj.save(os.path.join(ph_dir, ph_filename))
            flash('Photo uploaded and saved')
            if not pet_in_db:
                # if no profile exists, add a new object
                pet = Pet(petname=form.petname.data, petimage=ph_filename, petage=form.petage.data,
                          pettype=form.pettype.data,user=user_in_db)
                db.session.add(pet)
            else:
                pet_in_db.petimage = ph_filename
                pet_in_db.petage = form.petage.data
                pet_in_db.pettype = form.pettype.data
            # remember to commit
            db.session.commit()
            return redirect(url_for('pets.myPets'))
        else:
            return render_template('pets/petcenter.html', title='petcenter', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect('/login')
	
@pets.route('/treatPet', methods=['GET', 'POST'])
def addPet():
    form=PetForm()
    if not session.get("USERNAME") is None:
        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        if form.validate_on_submit():
            pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
            ph_dir = Config.PH_UPLOAD_DIR
            file_obj = form.petimage.data
            ph_filename = form.petname.data + '_PPH.jpg'
            file_obj.save(os.path.join(ph_dir, ph_filename))
            flash('Photo uploaded and saved')
            if not pet_in_db:
                # if no profile exists, add a new object
                pet = Pet(petname=form.petname.data, petimage=ph_filename, petage=form.petage.data,
                          pettype=form.pettype.data)
                db.session.add(pet)
            else:
                pet_in_db.petimage = ph_filename
                pet_in_db.petage = form.petage.data
                pet_in_db.pettype = form.pettype.data
            # remember to commit
            db.session.commit()
            return redirect(url_for('pets.myPets'))
        else:
            return render_template('pets/treatPet.html', title='TreatPet', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect('/login')


@pets.route('/myPets')
def myPets():
    pets = Pet.read_all()
    if pets is not None:
        return render_template('pets/myPets.html', title='myPets', pets=pets)
    else:
        return render_template('pets/myPets.html', title='myPets', pets=None)