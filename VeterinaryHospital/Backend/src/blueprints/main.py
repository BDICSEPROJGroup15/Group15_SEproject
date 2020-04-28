from flask import Blueprint, session, render_template, flash, redirect, url_for,request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from src.Models.Users import User
from src.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm
from flask_dropzone import random_filename
from src.Models.Users import Pet
from src.extension import db
import os
from flask import current_app
from src.utilize import current_user
main=Blueprint('main',__name__,url_prefix="/main")


@main.route('/')
@main.route('/index',methods=['POST','GET'])
def upload():

    if request.method=='POST' and 'file' in request.files:
        f= request.files.get('file')
        filename=random_filename(f.filename)
        f.save(os.path.join(current_app.config['PET_UPLOAD_PATH'],filename))
        pet = Pet(petimage=filename,user=current_user())
        db.session.add(pet)
        db.session.commit()
        print("PET STORED  success")
    return render_template('pet/upload.html')






