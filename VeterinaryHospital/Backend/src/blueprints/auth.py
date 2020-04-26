from flask import Blueprint, session, render_template, flash, redirect, url_for,request,jsonify
from werkzeug.security import check_password_hash, generate_password_hash

from src.Models.Pets import Pet
from src.extension import db
from src.Models.Users import User
from src.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm, PetForm, ProfileForm


auth=Blueprint('auth',__name__,url_prefix='/auth')
#
# @auth.route('/')
# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user_in_db = User.query.filter(User.username == form.username.data).first()
#         if not user_in_db:
#             flash('Wrong username or password, please check again')
#             return redirect(url_for('.redirect_page', page='login'))
#         if check_password_hash(user_in_db.password_hash, form.password.data):
#             session["USERNAME"] = user_in_db.username
#             if form.remember_me.data:
#                 session.permanent = True
#             flash('Login successfully')
#             return redirect(url_for('.redirect_page', page='index'))
#         flash('Incorrect Password')
#         return redirect(url_for('.redirect_page', page='login'))
#     return render_template('auth/login.html', title='Sign In', form=form)
#
#
# @auth.route('/signup', methods=['GET', 'POST'])
# def signup():
#     form = SignupForm()
#     print(form.validate_on_submit())
#     if form.validate_on_submit():
#         if form.password.data != form.password2.data:
#             flash('Passwords do not match!')
#             return redirect(url_for('.redirect_page', page='signup'))
#         passw_hash = generate_password_hash(form.password.data)
#         user = User(username=form.username.data, email=form.email.data, password_hash=passw_hash, administrator=False)
#         db.session.add(user)
#         db.session.commit()
#         session["USERNAME"] = user.username
#         flash('signup successfully')
#         return redirect(url_for('.redirect_page', page='index'))
#     return render_template('auth/signup.html', title='Register a new user', form=form)
#
#
# @auth.route('/logout')
# def logout():
#     session.pop("USERNAME", None)
#     return redirect(url_for('.login'))
#
#
# @auth.route('/checkuser', methods=['POST'])
# def check_username():
#     chosen_name = request.form['username']
#     user_in_db = User.query.filter(User.username == chosen_name).first()
#     if not user_in_db:
#         return jsonify({'returnvalue': 0})
#     else:
#         return jsonify({'returvalue': 1})
#
#
# # @app.route('/treatPet', methods=['GET', 'POST'])
# # def addPet():
# #     form = PetForm()
# #     if not session.get("USERNAME") is None:
# #         user_in_db = User.query.filter(User.username == session.get("USERNAME")).first()
# #         if form.validate_on_submit():
# #             pet_in_db = Pet.query.filter(Pet.petname == form.petname.data).first()
# #             ph_dir = Config.PH_UPLOAD_DIR
# #             file_obj = form.petimage.data
# #             ph_filename = form.petname.data + '_PPH.jpg'
# #             file_obj.save(os.path.join(ph_dir, ph_filename))
# #             flash('Photo uploaded and saved')
# #             if not pet_in_db:
# #                 # if no profile exists, add a new object
# #                 pet = Pet(petname=form.petname.data, petimage=ph_filename, petage=form.petage.data,
# #                           pettype=form.pettype.data)
# #                 db.session.add(pet)
# #             else:
# #                 pet_in_db.petimage = ph_filename
# #                 pet_in_db.petage = form.petage.data
# #                 pet_in_db.pettype = form.pettype.data
# #             # remember to commit
# #             db.session.commit()
# #             return redirect(url_for('myPets'))
# #         else:
# #             return render_template('treatPet.html', title='TreatPet', form=form)
# #     else:
# #         flash("User needs to either login or sign up first")
# #         return redirect('/login')
#
#
# # else:
# #     flash("User needs to either login or signup first")
# #     return redirect(url_for('login'))
#
#
# @auth.route('/profile', methods=['GET', 'POST'])
# def profile():
#     form = ProfileForm()
#     if not session.get("USERNAME") is None:
#
#         cur_user = User.query.filter(User.username == session.get("USERNAME")).first()
#         if form.validate_on_submit():
#             user_in_db = User.query.filter(User.username == form.name.data).first()
#             name_input = form.name.data
#             # profile_input=form.profile.data
#             # ph_dir = Config.PH_UPLOAD_DIR
#             # ph_filename = form.petname.data + '_PPH.jpg'
#             # profile_input.save(os.path.join(ph_dir, ph_filename))
#             # flash('Photo uploaded and saved')
#             if not user_in_db:
#                 cur_user.username = name_input
#                 db.session.add(cur_user)
#             else:
#                 flash('Username In Use')
#             db.session.commit()
#             session['USERNAME'] = cur_user.username
#             print("hello")
#             return redirect(url_for('main.index'))
#         else:
#             print("hello")
#             return render_template('auth/profile.html', title='profile', form=form)
#     else:
#         flash("User needs to either login or sign up first")
#         return redirect('login')
#
#
# @auth.route('/reset_password_request', methods=['GET', 'POST'])
# def reset_password_request():
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         print(user)
#         if not user:
#             flash('No available email')
#             return redirect(url_for('redirect_page', page='reset_password_request'))
#         send_password_reset_email(user)
#         flash('Please check your email')
#         return redirect(url_for('.redirect_page', page='login'))
#     return render_template('auth/reset_password_request.html', title='reset password', form=form)
#
#
# @auth.route('/reset_password', methods=['GET', 'POST'])
# def reset_password():
#     token0 = request.args.get("token")
#     print(token0)
#     user = User.verify_jwt_token(token0)
#     print(user)
#     if not user:
#         return redirect(url_for('main.index'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         print(str(user))
#         user_in_db = User.query.filter(User.username == str(user)).first()
#         user_in_db.password_hash = generate_password_hash(form.password.data)
#         db.session.commit()
#         flash('reset successfully')
#         return redirect(url_for('.redirect_page', page='login'))
#     return render_template('auth/reset_password.html', form=form)
#
#
# @auth.route('/redirect_page/<page>')
# def redirect_page(page):
#     return render_template('auth/redirect_page.html', page=page)
#     # retu
#     # return page