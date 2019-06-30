from datetime import datetime
from flask_login import UserMixin
import werkzeug.security as ws
from app import db, login

"""
flask-login LoginManager requires the User model class to implement the following properties:
* is_authenticated
* is_active
* is_anonymous
* get_id
Those can be implemented manually, but a generic implementation is alos provided in the form of
a mixin - UserMixin
"""
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    @login.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def set_password(self, password):
        self.password_hash = ws.generate_password_hash(password)

    def check_password(self, password):
        return ws.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
