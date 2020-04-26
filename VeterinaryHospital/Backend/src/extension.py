from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mail=Mail()
moment=Moment()
db=SQLAlchemy()
bootstrap=Bootstrap()
migrate=Migrate()

