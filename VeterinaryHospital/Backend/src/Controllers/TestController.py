

from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm
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


@app.route('/')
@app.route('/test')
def test():
    return render_template('outline.html', title='Test')
