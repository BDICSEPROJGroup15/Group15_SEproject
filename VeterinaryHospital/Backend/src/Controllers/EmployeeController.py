
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


@app.route('/petCenter', methods=['GET', 'POST'])
def petCenter():
    # if not session.get("USERNAME") is None:
    return render_template('staff/petCenter.html')
