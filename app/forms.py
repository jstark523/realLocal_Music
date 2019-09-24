from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class newArtistForm(FlaskForm):
    name = StringField("Artist Name", validators=[DataRequired()])
    town = StringField("Hometown", validators=[DataRequired()])
    bio = TextAreaField("Artist's Description", validators=[DataRequired()])
    submit = SubmitField("Submit")
