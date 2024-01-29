from flask import render_template, flash, redirect, url_for, session
from . import dashboard_bp
from users.views import login_required

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    if 'first_name' in session:
        first_name = session['first_name']
        return render_template('dashboard.html', first_name=first_name)
    else:
        flash('Adgang nægtet', 'error')
    return redirect(url_for('users.login'))
