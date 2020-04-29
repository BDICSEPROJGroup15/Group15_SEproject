from flask import Blueprint, render_template, session, flash, redirect

from src import Pet
from src.Utility.utilize import current_user

admin=Blueprint('admin',__name__)

@admin.route("/petcenter")
def index():
    if not session.get("USERNAME") is None:
        return render_template("admin/index.html")
    else:
        flash("User needs to either login or sign up first")
        return redirect('auth.login')

