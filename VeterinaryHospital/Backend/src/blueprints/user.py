from flask import Blueprint, render_template, send_from_directory, current_app,session,redirect,flash
from src.utilize import current_user
from src.Models.Pets import Pet
user=Blueprint('user',__name__,url_prefix="/user")

@user.route("/")
@user.route("/index")
def index():
    if not session.get("USERNAME") is None:
        current = current_user()
        pets = Pet.get_user_pet(current.id)
        print(pets)
        return render_template("profile.html", user=current, pets=pets)
    else:
        flash("User needs to either login or sign up first")
        return redirect('/login')


@user.route('/avatars/<filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'],filename)

@user.route('/pet/<filename>')
def get_pet_image(filename):
    return send_from_directory(current_app.config['PET_UPLOAD_PATH'],filename)