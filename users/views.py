from flask import render_template
from . import users_bp
from .forms import SignupForm

@users_bp.route('/signup')
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)