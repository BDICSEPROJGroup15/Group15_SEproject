from flask import Blueprint, render_template, session, flash, redirect,request
from src.Utility.reservation_list import reservation_list
from src.Models.Users import User
from src.Models.Reservations import Reservation
from src import Pet
from src.Utility.utilize import current_user

admin=Blueprint('admin',__name__)

@admin.route("/petcenter")
def index():
    if not session.get("USERNAME") is None:
        reservations=Reservation.read_all()
        user=current_user()
        return render_template("admin/index.html",reservations=reservations,user=user)
    else:
        flash("User needs to either login or sign up first")
        return redirect('auth.login')

