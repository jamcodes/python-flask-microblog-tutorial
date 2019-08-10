from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
# translate the login required messages
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
babel = Babel()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    app.register_blueprint(errors_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    # Flask uses python logging module for error-logging. All we need to do
    # to receive email notifications about errors is to configure the SMTPHandler.
    # To debug the mail server locally start a python smtp server:
    # python -m smtpd -n -c DebuggingServer localhost:8025
    # and set the server configuration variables:
    # MAIL_SERVER=localhost
    # MAIL_PORT=8025
    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'],
                subject='Microblog Failure',
                credentials=auth,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')

    return app


@babel.localeselector
def get_locale():
    '''Selects a best-match locale based on the Accept-Language header
sent by the user.
To make use of locale it is necessary to wrap every localizable text with a `_()` function.
Some string literals are assigned outsize of a request - the evaluation needs to be delayed
until it is used (which means it's under a request), this is done using `lazy_gettext()`,
it can be aliased to something like `_l()` to resemble the other wrapper.
A `babel.cfg` config file then needs to be provided if we need to translate text in Jinja templates.
The wrapped text then needs to be extracted into a .pot file:
  $ pybabel extract -F babel.cfg -k _l -o messages.pot .
Languange catalogs then need to be created:
  $ pybabel init -i messages.pot -d app/translations -l pl
This creates a .po file, which will need to have every string (wrapped with _() or _l()) translated
manually. Once translated the .po file needs to be compiled:
  $ pybabel compile -d app/translations
Only example translations are provided for the index home page.
'''
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    # For debugging just return the desired locale
    return 'pl'
