import os
from dotenv import load_dotenv

_basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(_basedir, '.flaskenv'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'default-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(_basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add email server details to be able to receive emial notifications about errors
    # These email server config variables are compatible with flask-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 3
    LANGUAGES = ['en', 'pl']
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
