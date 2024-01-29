from flask import render_template, flash, redirect, url_for
from . import dashboard_bp

@dashboard_bp('/dashboard')
def dashboard():
    return render_template('dashboard.html')