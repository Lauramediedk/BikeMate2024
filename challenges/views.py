from flask import render_template, flash, redirect, url_for
from . import challenges_bp
from .models import get_challenges


@challenges_bp.route('/', methods=['GET', 'POST'])
def challenges():
    try:
        challenges = get_challenges()

        if challenges:
            return render_template('challenges.html', challenges=challenges)
        else:
            flash('Ingen challenges fundet', 'info')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
    return render_template('challenges.html', challenges=[])
