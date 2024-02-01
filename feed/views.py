from . import feed_bp
from flask import render_template

@feed_bp.route('/')
def feed():
    return render_template('feed.html')