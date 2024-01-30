from flask import render_template, flash
from . import challenges_bp
from .models import get_challenges
from users.views import login_required


@challenges_bp.route('/', methods=['GET', 'POST'])
@login_required
def challenges():
    try:
        challenges = get_challenges()

        if challenges:
            for challenge in challenges:
                challenge['created_formatted'] = challenge['created'].strftime('%d. %m. %Y')
                challenge['expires_formatted'] = challenge['expires'].strftime('%d. %m. %Y')

            return render_template('challenges.html', challenges=challenges)
        else:
            flash('Ingen udfordringer i øjeblikket', 'info')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
    return render_template('challenges.html')
