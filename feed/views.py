from . import feed_bp
from flask import render_template
from users.views import login_required

@feed_bp.route('/')
@login_required
def feed():
    return render_template('feed.html', active_page='feed')