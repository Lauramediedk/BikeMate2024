from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, ValidationError


class EventForm(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(
        min=2, max=20)])
    description = TextAreaField('Beskrivelse', validators=[InputRequired(), Length(
        min=2, max=20)])
    startdate = DateField('Starts dato', format='%Y-%m-%d')
    enddate = DateField('Slut dato', format='%Y-%m-%d')
    location = StringField('Lokation', validators=[InputRequired(), Length(
        min=2, max=20)])
    submit = SubmitField('Gem')

    def validate_enddate(form, field):
        if field.data < form.startdate.data:
            raise ValidationError("Slut dato må ikke være før start dato.")
