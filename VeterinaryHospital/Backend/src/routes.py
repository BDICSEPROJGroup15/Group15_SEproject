from flask import render_template, flash, redirect, url_for, session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src import app, db
from src.forms import LoginForm, SignupForm,PetForm
from src.models import User,Pet
from src.forms import LoginForm, SignupForm
from src.models import User
from src.config import Config
import os


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_in_db = User.query.filter(User.username == form.username.data).first()
        if not user_in_db:
            flash('Wrong username or password, please check again')
            return redirect(url_for('login'))
        if check_password_hash(user_in_db.password_hash, form.password.data):
            session["USERNAME"] = user_in_db.username
            return redirect(url_for('index'))
        flash('Incorrect Password')
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            flash('Passwords do not match!')
            return redirect(url_for('signup'))
        passw_hash = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password_hash=passw_hash, administrator=False)
        db.session.add(user)
        db.session.commit()
        session["USERNAME"] = user.username
        return redirect(url_for('index'))
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
        return jsonify({'returvalue': 1})
@app.route('/test',methods=['GET','POST'])
def test():
        return jsonify('pong!')


@app.route('/treatPet',methods=['GET','POST'])
def treatPet():
	form=PetForm()
	if not session.get("USERNAME") is None:
		if form.validate_on_submit():
			pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
			ph_dir=Config.PH_UPLOAD_DIR
			file_obj=form.petimage.data
			ph_filename=form.petname.data+'_PPH.jpg'
			file_obj.save(os.path.join(ph_dir, ph_filename))
			flash('Photo uploaded and saved')
			if not pet_in_db:
				# if no profile exists, add a new object
				pet=Pet(petname=form.petname.data,petimage=ph_filename,petage=form.petage.data,pettype=form.pettype.data)
				db.session.add(pet)
			else:
				pet_in_db.petimage=ph_filename
				pet_in_db.petage=form.petage.data
				pet_in_db.pettype=form.pettype.data
			# remember to commit	
			db.session.commit()
			return redirect(url_for('myPets'))
		else:
			return render_template('treatPet.html', title='TreatPet', form=form)
	else:
		flash("User needs to either login or sign up first")
		return redirect('/login')


@app.route('/myPets')
def myPets():
	pets=Pet.query.all()
	return render_template('myPets.html', title='myPets', posts=pets)
	
	
@app.route('/petCenter', methods=['GET', 'POST'])
def petCenter():
    # if not session.get("USERNAME") is None:
        return render_template('petCenter.html')
    # else:
    #     flash("User needs to either login or signup first")
    #     return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # if not session.get("USERNAME") is None:
        return render_template('profile.html')
    # else:
    #     flash("User needs to either login or signup first")
    #     return redirect(url_for('login'))


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    # if not session.get("USERNAME") is None:
        return render_template('reservation.html')
    # else:
    #     flash("User needs to either login or signup first")
    #     return redirect(url_for('login'))


@app.route('/chatRoom', methods=['GET', 'POST'])
def chatRoom():
    # if not session.get("USERNAME") is None:
        return render_template('chatRoom.html')
    # else:
    #     flash("User needs to either login or signup first")
    #     return redirect(url_for('login'))
