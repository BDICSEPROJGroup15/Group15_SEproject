from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm, AddReservation, EditReservation, \
    AddReservationForm
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Models.Users import User
from flask import render_template, flash, redirect, url_for, session, request, jsonify, abort, make_response, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from src.extension import db
from src.Models.Pets import Pet
from src.Models.Reservations import Reservation
from config import Config
import os
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.decoration import *

auth=Blueprint('auth',__name__)

@auth.route('/')
@auth.route('/index')
def index():
    return render_template('WelcomePage.html', title='Home')


@auth.route('/login', methods=['GET', 'POST'])
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


@auth.route('/signup', methods=['GET', 'POST'])
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


@auth.route('/logout')
def logout():
    session.pop("USERNAME", None)
    return redirect(url_for('login'))


@auth.route('/checkuser', methods=['POST'])
def check_username():
    chosen_name = request.form['username']
    user_in_db = User.query.filter(User.username == chosen_name).first()
    if not user_in_db:
        return jsonify({'returnvalue': 0})
    else:
        return jsonify({'returnvalue': 1})

@auth.route('/checkemail', methods=['POST'])
def check_email():
    chosen_email = request.form['email']
    email = User.query.filter(User.email == chosen_email).first()
    if not email:
        return jsonify({'emailreturnvalue': 0})
    else:
        return jsonify({'emailreturnvalue': 1})


@auth.route('/chatRoom', methods=['GET', 'POST'])
def chatRoom():
    # if not session.get("USERNAME") is None:
    return render_template('chatRoom.html')


@auth.route('/reset_password_request', methods=['GET', 'POST'])
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


@auth.route('/reset_password', methods=['GET', 'POST'])
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


@auth.route('/redirect_page/<page>')
def redirect_page(page):
    return render_template('redirect_page.html', page=page)
    # return page