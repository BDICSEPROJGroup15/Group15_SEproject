from flask import Flask
from blogapp.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# enable CORS
CORS(app, resources = {r'/*': {'origins':'*'}})





from blogapp import routes, models

