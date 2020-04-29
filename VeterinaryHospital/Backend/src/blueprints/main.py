from flask import Blueprint, session, render_template, flash, redirect, url_for, request, jsonify, send_from_directory
from src.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm, PetForm
from flask_dropzone import random_filename
from src.Models.Users import Pet
from src.extension import db
import os
from flask import current_app
from src.Utility.utilize import current_user
main=Blueprint('main',__name__,url_prefix="/main")



@main.route('/upload', methods=['POST', 'GET'])
def upload():
    if not session.get("USERNAME") is None:
        global filename
        if request.method == 'POST' and 'file' in request.files:
            f = request.files.get('file')
            filename = random_filename(f.filename)
            f.save(os.path.join(current_app.config['PET_UPLOAD_PATH'], filename))
            form = PetForm()
        form=PetForm()
        if form.validate_on_submit():
            print("hello2")
            pet = Pet(petname=form.petname.data,petage=form.petage.data,pettype=form.pettype.data,petimage=filename,user=current_user())
            db.session.add(pet)
            db.session.commit()
            print("PET STORED  success")
            return redirect(url_for('.index'))
        else:
            return render_template('main/treatPet.html', title='TreatPet', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect(url_for('auth.login'))

@main.route("/")
@main.route("/index")
def index():
    if not session.get("USERNAME") is None:
        current = current_user()
        pets = Pet.get_user_pet(current.id)

        return render_template("main/mypets.html", user=current, pets=pets)
    else:
        flash("User needs to either login or sign up first")
        return redirect(url_for('auth.login'))


@main.route('/avatars/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

@main.route('/pet/<filename>')
def get_pet_image(filename):
    return send_from_directory(current_app.config['PET_UPLOAD_PATH'],filename)



