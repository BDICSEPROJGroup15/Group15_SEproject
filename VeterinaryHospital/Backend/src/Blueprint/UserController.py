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
from src.decoration import *



@app.route('/')
@app.route('/index')
def index():
    return render_template('WelcomePage.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('Wrong username or password, please check again')
            return redirect(url_for('redirect_page', page='login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            session["USERNAME"] = user_in_db.username
            if form.remember_me.data:
                session.permanent = True
            flash('Login successfully')
            return redirect(url_for('redirect_page', page='index'))
        flash('Incorrect Password')
        return redirect(url_for('redirect_page', page='login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('redirect_page', page='signup'))
        passw_hash = generate_password_hash(form.password.data)
        # user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash, administrator=False)
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash)
        db.session.add(user)
        db.session.commit()
        session["USERNAME"] = user.username
        flash('signup successfully')
        return redirect(url_for('redirect_page', page='index'))
    return render_template('signup.html', title='Register a new user', form=form)


@app.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('login'))


@app.route('/checkuser', methods=['POST'])
def check_username():
    chosen_name = request.form['username']
    user_in_db = User.query.filter(User.username == chosen_name).first()
    if not user_in_db:
        return jsonify({'returnvalue': 0})
    else:
        return jsonify({'returnvalue': 1})

@app.route('/checkemail', methods=['POST'])
def check_email():
    chosen_email = request.form['email']
    email = User.query.filter(User.email == chosen_email).first()
    if not email:
        return jsonify({'emailreturnvalue': 0})
    else:
        return jsonify({'emailreturnvalue': 1})

@app.route('/treatPet', methods=['GET', 'POST'])
def addPet():
    form = PetForm()
    if not session.get("USERNAME") is None:
        # user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        # if form.validate_on_submit():
        #     pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
        #     ph_dir = Config.PH_UPLOAD_DIR
        #     file_obj = form.petimage.data
        #     ph_filename = form.petname.data + '_PPH.jpg'
        #     file_obj.save(os.path.join(ph_dir, ph_filename))
        #     flash('Photo uploaded and saved')
        #     if not pet_in_db:
        #         # if no profile exists, add a new object
        #         pet = Pet(petname=form.petname.data, petimage=ph_filename, petage=form.petage.data,
        #                   pettype=form.pettype.data)
        #         db.session.add(pet)
        #     else:
        #         pet_in_db.petimage = ph_filename
        #         pet_in_db.petage = form.petage.data
        #         pet_in_db.pettype = form.pettype.data
        #     # remember to commit
        #     db.session.commit()
        #     return redirect(url_for('myPets'))
        # else:
            return render_template('treatPet.html', title='TreatPet', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect('/login')


@app.route('/myPets')
def myPets():
    pets = Pet.read_all()
    if pets is not None:
        return render_template('myPets.html', title='myPets', pets=pets)
    else:
        return render_template('myPets.html', title='myPets', pets=None)



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
            # print("hello")
            return redirect(url_for('index'))
        else:
            # print("hello")
            return render_template('profile.html', title='profile', form=form)
    else:
        flash("User needs to either login or sign up first")
        return redirect('login')



@app.route('/chatRoom', methods=['GET', 'POST'])
def chatRoom():
    # if not session.get("USERNAME") is None:
    return render_template('chatRoom.html')


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if not user:
            flash('No available email')
            return redirect(url_for('redirect_page', page='reset_password_request'))
        send_password_reset_email(user)
        flash('Please check your email')
        return redirect(url_for('redirect_page', page='login'))
    return render_template('reset_password_request.html', title='reset password', form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    token0 = request.args.get("token")
    print(token0)
    user = User.verify_jwt_token(token0)
    print(user)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        print(str(user))
        user_in_db = User.query.filter(User.username == str(user)).first()
        user_in_db.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('reset successfully')
        return redirect(url_for('redirect_page', page='login'))
    return render_template('reset_password.html', form=form)


@app.route('/redirect_page/<page>')
def redirect_page(page):
    return render_template('redirect_page.html', page=page)
    # return page