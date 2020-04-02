from email.mime import application

from flask import Flask


from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import sys
sys.path.append('..')
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
mail = Mail(app)
# Scss(app,static_dir='static/style/scss2css', asset_dir='assets')
#


def create_app(test_config=None):
    mail.init_app(application)


# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# 用户模块 User Module
from src.Controllers import UserController
