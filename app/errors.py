from flask import render_template
from app import app, db


@app.errorhandler(404)
def not_found_error(error):
    # view functions return a return code as the second value
    # the default is 200 - successful response (which is why for regular view
    # functions we don't need to specify it explicitly)
    # For error-pages we return the corresponding error code explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()   # make sure we don't corrupt the database
    return render_template('500.html'), 500
