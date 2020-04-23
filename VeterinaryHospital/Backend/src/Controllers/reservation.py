from flask import Blueprint, render_template, request

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


@reservation.route('/show')
def show():
    form = AddReservationForm()
    all_reservations = Reservation.read_all()
    r=request.args.get("r")
    if r:
        r = int(r)
        for res in all_reservations:
            if r==res.id:
                Reservation.remove_res(r)
                all_reservations = Reservation.read_all()
    for res in all_reservations:
        Reservation.set_user_pet_name(res,User.get_user(res.user_id),Pet.get_pet(res.pet_id))
    print(all_reservations)

    return render_template('reservation/show.html',reservations=all_reservations)


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
@reservation.route('/reservation/list/', methods=['GET', 'POST'])
def list():
    form = AddReservationForm()
    # print("reservation add")
    if not session.get("USERNAME") is None:
        print(form.validate_on_submit())
        resObjects = Reservation.query.filter_by(username=session.get('USERNAME'))
        if form.validate_on_submit():
            print("reservation add")
            petname = "jojo"
            name = "arno"
            Email = "guiwecgdiu@163.com"
            Status = "Waiting"

            Reservation.add_res(None, None, form.treattype.data, 'Beijing', True)
            return render_template('reservation/list.html', resObjects=resObjects, add=True, form=form, petname=petname,
                                   name=name, Email=Email, Status=Status)

        return render_template('reservation/list.html', resObjects=resObjects, form=form, add=None)
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
