from flask import render_template, flash, redirect, url_for, session, request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from src import app, db
from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm
from src.models import User, Pet
from config import Config
import os

from src.email import send_password_reset_email
from src.forms import ResetPasswordRequestForm


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
            if form.remember_me.data:
                session.permanent = True
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
        user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash, administrator=False)
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


@app.route('/test', methods=['GET', 'POST'])
def test():
    return jsonify('pong!')


@app.route('/treatPet', methods=['GET', 'POST'])
def treatPet():
    form = PetForm()
    if not session.get("USERNAME") is None:
        user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
        if form.validate_on_submit():
            pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
            ph_dir = Config.PH_UPLOAD_DIR
            file_obj = form.petimage.data
            ph_filename = form.petname.data + '_PPH.jpg'
            file_obj.save(os.path.join(ph_dir, ph_filename))
            flash('Photo uploaded and saved')
            if not pet_in_db:
                # if no profile exists, add a new object
                pet = Pet(petname=form.petname.data, petimage=ph_filename, petage=form.petage.data,
                          pettype=form.pettype.data, petowner=user_in_db.username)
                db.session.add(pet)
            else:
                pet_in_db.petimage = ph_filename
                pet_in_db.petage = form.petage.data
                pet_in_db.pettype = form.pettype.data
                pet_in_db.petowner = user_in_db.username
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
    pets = Pet.query.filter(Pet.petowner == session.get("USERNAME")).all()
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
    if not session.get("USERNAME") is None:

        return render_template('reservation.html')
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


@app.route('/chatRoom', methods=['GET', 'POST'])
def chatRoom():
    # if not session.get("USERNAME") is None:
    return render_template('chatRoom.html')


# else:
#     flash("User needs to either login or signup first")
#     return redirect(url_for('login'))


tasks = [
    {
        "id": 1,
        "title": u'Buy groceries',
        "description": u'Milk, Cheese, Pizza, Fruit, Tylenol',
        "done": False
    },
    {
        "id": 2,
        "title": "Learn Python",
        "description": "Need to find a good Python tutorial on the web",
        'done': False
    }
]


# Accessible Api Arno Li 2020/3/29
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    # if not session.get("USERNAME") is None:
    return jsonify('task', tasks)


# else:
#     flash("User needs to either login or signup first")
#     return redirect(url_for('login'))

@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = list(filter(lambda t: t['id'] == task_id, tasks))
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)
#
# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error':'bad_request'}),400)


# curl syntax have some errors 3/29/2020
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    # if not request.json or not "title" in request.json:
    #     abort(400)
    # task = {
    #     'id': tasks[-1]['id'] + 1,
    #     # 'title': request.json["title"],
    #     # 'description': request.json.get('description', ''),
    #     'done': False
    #     }
    test = request.json
    # tasks.append({"id":"100"})
    # print(tasks)
    return jsonify(test)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if not user:
            flash('No available email')
            return redirect(url_for('reset_password_request'))
        send_password_reset_email(user)
        flash('Please check your email')
        return redirect(url_for('login'))
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
        user_in_db = User.query.filter(User.username == str(user)).first()
        user_in_db.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('reset successfully')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
