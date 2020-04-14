

from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm
from src.Models.Users import User
from flask import render_template, flash, redirect, url_for, session, request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from src import app, db
from src.Models.Pets import Pet
from config import Config
import os
from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm



@app.route('/res')
def res():
    return render_template('reservation.html', title='reservation')

@app.route('/chatbox')
def charRoom():
    return render_template('chatbox.html',title='ChatRoom')

@app.route('/pro')
def canlender():
    return app.send_static_file('html/res_canlender.html')

@app.route('/test')
def form():
    return render_template('staff_panel/test.html')