from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import InputRequired, Length, ValidationError


class EventForm(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Titel"})
    description = TextAreaField('Beskrivelse', validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Beskrivelse"})
    startdate = DateField('Dato', validators=[InputRequired()])
    location = StringField('Lokation', validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Lokation"})
    submit = SubmitField('Opret event')

    def validate_enddate(form, field):
        if field.data < form.startdate.data:
            raise ValidationError("Slut dato må ikke være før start dato.")
