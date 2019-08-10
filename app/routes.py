from app import app
from app.translate import translate
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug import urls
from app import forms, models, forms, db, email
from datetime import datetime
from flask_babel import _, get_locale
from guess_language import guess_language











