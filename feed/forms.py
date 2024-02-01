from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import InputRequired, length

class PostForm(FlaskForm):
    content = TextAreaField('Indhold', validators=[length(max=2000)], render_kw={'placeholder': 'Skriv et opslag'})
    image_path = StringField('Upload billede')
    is_private = BooleanField('Privat', render_kw={'class': 'checkbox'})
    submit = SubmitField('Slå op')