from flask import render_template
from . import users_bp

@users_bp.route('/signup')
def signup():
    return "I will sign up at some point!"