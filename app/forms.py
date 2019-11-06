from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, PasswordField, BooleanField, DateField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class newArtistForm(FlaskForm):
    name = StringField("Artist Name", validators=[DataRequired()])
    town = StringField("Hometown", validators=[DataRequired()])
    bio = TextAreaField("Artist's Description", validators=[DataRequired()])
    submit = SubmitField("Submit")

class newVenueForm(FlaskForm):
    name = StringField("Venue Name", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Submit")

class newEventForm(FlaskForm):
    name = StringField("Event Name", validators=[DataRequired()])
    when = DateField('Start Date', format='%m/%d/%Y %H:%M', validators=[DataRequired()])
    venue = SelectField("Venue", coerce= int, validators=[DataRequired()])
    artists = SelectMultipleField("Artists", coerce=int, validators=[DataRequired()])
    submit = SubmitField("Submit")

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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
