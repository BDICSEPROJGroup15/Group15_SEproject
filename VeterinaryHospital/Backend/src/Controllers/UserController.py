from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm, AddReservation, EditReservation, \
    AddReservationForm
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Models.Users import User
from flask import render_template, flash, redirect, url_for, session, request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from src import app, db
from src.Models.Pets import Pet
from src.Models.Reservations import Reservation
from config import Config
import os
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Controllers.reservation_bp import reservation_bp
from src.Controllers.pets_bp import pet_bp
from src.Controllers.auth_bp import auth_bp
from src.Controllers.user_bp import user_bp

# Blueprint Registering
app.register_blueprint(reservation_bp)
app.register_blueprint(pet_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)

@app.route('/')
@app.route('/index')
def index():
    return render_template('Welcomepage.html', title='Home')



# else:
#     flash("User needs to either login or signup first")
#     return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = ProfileForm()
    if not session.get("USERNAME") is None:

        cur_user = User.query.filter(User.username == session.get("USERNAME")).first()
        if form.validate_on_submit():
            user_in_db = User.query.filter(User.username == form.name.data).first()
            name_input = form.name.data
            # profile_input=form.profile.data
            # ph_dir = Config.PH_UPLOAD_DIR
            # ph_filename = form.petname.data + '_PPH.jpg'
            # profile_input.save(os.path.join(ph_dir, ph_filename))
            # flash('Photo uploaded and saved')
            if not user_in_db:
                cur_user.username = name_input
                db.session.add(cur_user)
            else:
                flash('Username In Use')
            db.session.commit()
            session['USERNAME'] = cur_user.username
            print("hello")
            return redirect(url_for('index'))
        else:
            print("hello")
            return render_template('profile.html', title='profile', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect('login')



@app.route('/chatRoom', methods=['GET', 'POST'])
def chatRoom():
    # if not session.get("USERNAME") is None:
    return render_template('chatRoom.html')


