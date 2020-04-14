from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, RadioField, FileField, \
    TextAreaField
from wtforms.validators import DataRequired, Email
from flask_wtf.file import FileRequired, FileAllowed


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProfileForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    # birth = DateField ('Date of Birth (format: YYYY-MM-DD)', format='%Y-%m-%d', validators = [DataRequired()])
    # profile=FileField('Profile',validators=[FileRequired(),FileAllowed(['jpg','png','svg'],'JPG,PNG,SVG')])
    submit = SubmitField('Update Profile')



class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    accept_rules = BooleanField('I accept the site rules', validators=[DataRequired()])
    submit = SubmitField('Register')
	
class PetForm(FlaskForm):
	petname = StringField('Petname', validators=[DataRequired()])
	petage = StringField('Petage', validators=[DataRequired()])
	pettype = StringField('Pettype', validators=[DataRequired()])
	petimage = FileField('Pet Image', validators = [FileRequired(),FileAllowed(['jpg'], 'Only JPG files please')])
	submit = SubmitField('Treat !.!')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    submit = SubmitField('send_email')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('reset')