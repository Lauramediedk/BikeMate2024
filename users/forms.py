from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired, length, email


class SignupForm(FlaskForm):
    """Form for the user signup"""
    first_name = StringField('Fornavn', validators=[InputRequired(), length(
        min=2, max=20)], render_kw={'placeholder': 'Fornavn'})
    last_name = StringField('Efternavn', validators=[InputRequired(), length(
        min=2, max=30)], render_kw={'placeholder': 'Efternavn'})
    email = EmailField('Email', validators=[InputRequired(), email(), length(
        min=7, max=20)], render_kw={'placeholder': 'Email'})
    password = PasswordField('Adgangskode', validators=[InputRequired(), length(
        min=8, max=16)], render_kw={'placeholder': 'Kodeord'})
    submit = SubmitField('Opret bruger')


class LoginForm(FlaskForm):
    """Form for login"""
    email = EmailField('Email', validators=[InputRequired(), email(), length(
        min=7, max=20)], render_kw={'placeholder': 'Email'})
    password = PasswordField('Adgangskode', validators=[InputRequired(), length(
        min=8, max=16)], render_kw={'placeholder': 'Kodeord'})
    submit = SubmitField('Log ind')
