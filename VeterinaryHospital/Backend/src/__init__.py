from flask_cors import CORS
import os
from src.setting import config
from flask import Flask,render_template,Blueprint
# from src.blueprints.auth import auth
# from src.blueprints.blog import blog
# from src.blueprints.main import main
# from src.blueprints.admin import admin
from src.extension import mail,db,moment,bootstrap




def create_app(config_name=None):
    if config_name is None:
        config_name=os.getenv('FLASK_CONFIG','development')

    app=Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    # enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    # register_blueprint(app)
    register_error(app)
    register_externsion(app)
    register_shell_context(app)
    register_logging(app)
    # register_commands(app)
    return app

#
# def register_blueprint(app):
#     app.register_blueprint(blueprint=auth)
#     app.register_blueprint(blueprint=blog)
#     app.register_blueprint(blueprint=main)
#     app.register_blueprint(blueprint=admin, url_prefix='/admin')


def register_logging(app):
    pass

def register_externsion(app):
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)

def register_error(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error/400.html'), 400

# def register_commands(app):
#     # .......
#     return ""
app=create_app(None)



# User Module
from src.Blueprint import UserController
from src.Blueprint import TestController

