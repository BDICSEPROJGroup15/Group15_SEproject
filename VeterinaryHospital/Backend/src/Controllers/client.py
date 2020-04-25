from flask import Blueprint, render_template, request
from src.Controllers import reservation_list
from src.Models.Users import User
from src.Models.Pets import Pet
from src.forms import LoginForm, SignupForm, PetForm, ResetPasswordForm, ProfileForm, AddReservation, EditReservation, \
    AddReservationForm
from flask import session, render_template, redirect, request, flash, url_for
from src import db
from src.Models.Reservations import Reservation


client = Blueprint('client', __name__, template_folder="/template/client",
                        static_folder='static/example', url_prefix='/client')

@client.route("/")
@client.route("/indx")
def home():
    return render_template("client/index.html")