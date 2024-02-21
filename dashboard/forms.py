from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import InputRequired

class BioForm(FlaskForm):
    """Description field for updating the users bio"""
    description = TextAreaField('Beskrivelse', validators=[InputRequired()])
    submit = SubmitField('Gem')
    cancel = SubmitField('Annuller')
