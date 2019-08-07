from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.') # translate the login required messages
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)


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
