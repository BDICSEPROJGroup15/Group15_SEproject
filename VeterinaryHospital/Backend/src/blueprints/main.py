from flask import Blueprint, session, render_template, flash, redirect, url_for,request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from src.Models.Users import User
from src.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm

main=Blueprint('main',__name__)


@main.route('/')
@main.route('/index')
def index():
    return "hello"






