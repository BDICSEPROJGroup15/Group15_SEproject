import os

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_EMAIL = ['ysytql@163.com']

    CV_UPLOAD_DIR = os.path.join(basedir, 'uploaded_CV')
    PH_UPLOAD_DIR = os.path.join(basedir, 'src', 'static', 'uploaded_PH')

    PET_UPLOAD_PATH=os.path.join(basedir,'uploads')

    MAIL_SERVER = 'smtp.163.com'
    MAIL_USERNAME = 'wsdsgbxd@163.com'
    MAIL_PASSWORD = 'VLEMBIFMETRSMLCJ'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_DEFAULT_SENDER = ('YSY', 'MAIL_USERNAME')

    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 1
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_ENABLE_CRSF = True

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'hospital.db')

class TestingConfig(BaseConfig):
    TESTING =True
    WTF_CSRF_ENABLED=False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'hospital.db')

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.db')


config= {
        'development':DevelopmentConfig,
        'testing':TestingConfig,
        'production':ProductionConfig
    }
