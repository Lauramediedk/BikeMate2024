from flask import render_template, flash
from . import users_bp
from .forms import SignupForm
from .models import User
from werkzeug.security import generate_password_hash


@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form=SignupForm()
    if form.validate_on_submit():
        try:
            user=User(
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
