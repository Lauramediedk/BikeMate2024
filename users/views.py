from functools import wraps
from flask import render_template, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from . import users_bp
from .forms import SignupForm, LoginForm
from .models import User


@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        try:
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                hashed_password=generate_password_hash(form.password.data)
            )
            user.signup_user()

            flash('Bruger oprettet', 'success')
        except RuntimeError as e:
            flash(f"Fejl ved oprettelsen: {str(e)}")

    return render_template('signup.html', form=form)


@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.find_user_email(form.email.data)
            if user and user.check_password(form.password.data):
                session['first_name'] = user.first_name
                flash('Log ind godkendt', 'success')
                return redirect(url_for('dashboard.dashboard'))
            else:
                flash('Log ind mislykkedes', 'error')

        except RuntimeError as e:
            flash(f"Fejl ved log ind: {str(e)}")
    return render_template('login.html', form=form)


def login_required(f):  # Make sure unauthorised users can't enter
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'first_name' in session:
            return f(*args, **kwargs)
        else:
            flash('Du skal logge ind først', 'error')
            return redirect(url_for('users.login'))
    return wrap

