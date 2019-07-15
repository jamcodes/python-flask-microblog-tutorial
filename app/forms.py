from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app import models


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # WTForms treats any methods named according to a pattern `validate_<field_name>`
    # as custom validators, and adds them to the validators list for the field.
    def validate_username(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken. Please use a different username.')

    def validate_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                'An account already exists for this email. Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = models.User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Username already exists. Please use a different one.')
