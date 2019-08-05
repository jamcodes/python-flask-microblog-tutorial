from app import app, routes, models, errors, db, cli
from app.models import User, Post
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler


@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'Post':Post}


# Flask uses python logging module for error-logging. All we need to do
# to receive email notifications about errors is to configure the SMTPHandler.
# To debug the mail server locally start a python smtp server:
# python -m smtpd -n -c DebuggingServer localhost:8025
# and set the server configuration variables:
# MAIL_SERVER=localhost
# MAIL_PORT=8025
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
