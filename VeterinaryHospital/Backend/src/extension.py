from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

mail=Mail()
moment=Moment()
db=SQLAlchemy()
bootstrap=Bootstrap()