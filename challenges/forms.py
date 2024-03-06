from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import InputRequired, Length


class EventForm(FlaskForm):
    title = StringField('Titel', validators=[InputRequired(), Length(
        min=2, max=40)], render_kw={"placeholder": "Titel"})
    description = TextAreaField('Beskrivelse', validators=[InputRequired()],
    render_kw={"placeholder": "Beskrivelse"})
    startdate = DateField('Starts dato', validators=[InputRequired()], format='%Y-%m-%d')
    location = StringField('Lokation', validators=[InputRequired(), Length(
        min=2, max=20)], render_kw={"placeholder": "Lokation"})
    submit = SubmitField('Opret event')