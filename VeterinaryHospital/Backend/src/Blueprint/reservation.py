from flask import Blueprint, render_template, request
from src.Blueprint import reservation_list
from src.Models.Users import User
from src.Models.Pets import Pet
from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm, AddReservation, EditReservation, \
    AddReservationForm
from flask import session, render_template, redirect, request, flash, url_for
from src import db
from src.Models.Reservations import Reservation

reservation = Blueprint('reservation', __name__, template_folder="/template/reservation",
                        static_folder='static/example', url_prefix='/reservation')


@reservation.route('/index')
def index():
    return render_template('reservation/add.html')


@reservation.route('/show', methods=['GET', 'POST'])
def show():
    state_list = []
    if request.form.getlist("state_list[]") is not None and request.form.getlist("state_list[]") != []:
        state_list = request.form.getlist("state_list[]")
        print(state_list)
        Reservation.update_state(state_list)
    all_reservations = Reservation.read_all()
    r = request.args.get("r")
    if request.form.getlist("id_list[]") is not None and request.form.getlist("id_list[]") != []:
        reservation_list.update_list(request.form.getlist("id_list[]"))
    # print(reservation_list.get_list())
    if r:
        r = int(r)
        for res in all_reservations:
            if r == res.id:
                Reservation.remove_res(r)
                all_reservations = Reservation.read_all()
    for res in all_reservations:
        Reservation.set_user_pet_name(res, User.get_user(res.user_id), Pet.get_pet(res.pet_id))
        Reservation.set_createTime(res)
    # print(all_reservations)
    # return render_template('reservation/show.html', reservations=all_reservations)
    return render_template('reservation/show.html', reservations=all_reservations, list=reservation_list.get_list())


# else:
#     flash("User needs to either login or signup first")
#     return redirect(url_for('login'))

# add reservation
@reservation.route('/reservation/add/', methods=['GET', 'POST'])
def add():
    # reservations=Reservation.query.filter_by(user_id=userid)
    form = AddReservation()
    if not session.get("USERNAME") is None:
        if form.validate_on_submit():
            petname = form.petname.data
            category = form.category.data
            reservation = Reservation(username=session.get('USERNAME'), petname=petname, type=category)
            db.session.add(reservation)
            db.session.commit()
            flash('Add a reservation')
            return redirect(url_for(url_for('list')))
        else:
            return render_template('reservation/add.html', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('app.login'))


# Edit reservtion
@reservation.route('/reservation/edit/<int:id>/', methods=['GET', 'POST'])
def edit(id):
    form = EditReservation()
    if not session.get("USERNAME") is None:
        reservation = Reservation.query.filter_by(id=id).first()
        form.petname = reservation.petname
        form.category.data = reservation.type
        if form.validate_on_submit():
            petname = request.form.get('petname')
            category = request.form.get('category')
            reservation.petname = petname
            reservation.category = category
            db.session.add(reservation)
            db.session.commit()
            return redirect(url_for(url_for('list')))
        else:
            return render_template('reservation/edit.html', form=form)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


# delete Reservation
# 删除任务: 根据任务id删除
@reservation.route('/todo/delete/<int:id>/')
def delete(id):
    if not session.get("USERNAME") is None:
        reservation = Reservation.query.filter_by(id=id).first()
        db.session.delete(reservation)
        db.session.commit()
        return redirect(url_for('list'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


# lookup reservatiok
@reservation.route('/list', methods=['GET', 'POST'])
def list():
    if not session.get("USERNAME") is None:
        user_in_db = User.query.filter(User.username == session["USERNAME"]).first()
        if request.form.getlist("res[]") is not None and request.form.getlist("res[]") != []:
            add_res = request.form.getlist("res[]")
            pet = User.query.filter(Pet.id == int(add_res[0])).first()
            print("add_res" + str(add_res))
            Reservation.add_res(user_in_db,pet,add_res[1],add_res[2],"surgery confirmed")

        if request.form.getlist("edit_res[]") is not None and request.form.getlist("edit_res[]") != []:
            edit_res=request.form.getlist("edit_res[]")
            pet = User.query.filter(Pet.id == int(edit_res[1])).first()
            print("edit_res: "+ str(edit_res))
            Reservation.update_res(int(edit_res[0]),pet,edit_res[2],edit_res[3])
        # print("username:"+str(user_in_db))
        reservation = Reservation.get_user_res(user_in_db.id)
        print("reservation: "+str(reservation))
        pet = Pet.get_user_pet(user_in_db.id)
        # print("pet:"+str(pet))
        for res in reservation:
            Reservation.set_user_pet_name(res, User.get_user(res.user_id), Pet.get_pet(res.pet_id))
            Reservation.set_createTime(res)
        return render_template('reservation/add.html', reservations=reservation, user=user_in_db, pets=pet)
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


# change task state
@reservation.route('/reservation/done/<int:id>/', methods=['GET', 'POST'])
def done(id):
    if not session.get("USERNAME") is None:
        reservation = Reservation.query.filter_by(id=id).first()
        reservation.state = "Ready to Release"
        db.session.add(reservation)
        db.commit()
        flash('Success')
        return redirect(url_for('list'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))


# change task state
@reservation.route('/reservation/undo/<int:id>/', methods=['GET', 'POST'])
def undo(id):
    if not session.get("USERNAME") is None:
        reservation = Reservation.query.filter_by(id=id).first()
        reservation.state = "Surgery Confirmed"
        db.session.add(reservation)
        db.commit()
        flash('Success')
        return redirect(url_for('list'))
    else:
        flash("User needs to either login or signup first")
        return redirect(url_for('login'))
