from flask import Blueprint
from src.Models.Reservations import Reservation


user_bp=Blueprint("user",__name__,url_prefix="/user")

@user_bp.route("/")
@user_bp.route("/hello")
def hello():
    return "hello"

