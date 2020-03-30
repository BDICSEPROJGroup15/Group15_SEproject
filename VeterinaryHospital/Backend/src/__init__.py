from email.mime import application

from flask import Flask


from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

<<<<<<< HEAD

=======
import sys
sys.path.append('..')
from config import Config
>>>>>>> 96aa9163aae68474c402761b31b09382bfcd8e46

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

mail = Mail(app)


def create_app(test_config=None):
    mail.init_app(application)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

from src import routes, models
