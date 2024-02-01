from flask import render_template, flash, session, request, redirect, url_for
from . import challenges_bp
from .models import get_challenges, join_challenges, check_if_joined
from users.views import login_required


@challenges_bp.route('/', methods=['GET', 'POST'])
@login_required
def challenges():
    try:
        if request.method == 'POST':
            user_id = session.get('user_id')
            challenge_id = request.form.get('challenge_id')

            if not check_if_joined(user_id, challenge_id):
                join_challenges(user_id, challenge_id)
                flash('Du har tilmeldt dig', 'success')
            else:
                flash('Du er allerede tilmeldt denne udfordring', 'info')

            return redirect(url_for('challenges.challenges'))

        else:
            challenges = get_challenges()

            if challenges:
                for challenge in challenges:
                    challenge['created_formatted'] = challenge['created'].strftime('%d. %m. %Y')
                    challenge['expires_formatted'] = challenge['expires'].strftime('%d. %m. %Y')
                    challenge['is_joined'] = check_if_joined(session.get('user_id'), challenge['challenge_id'])

                return render_template('challenges.html', challenges=challenges, active_page='challenges')
            else:
                flash('Ingen udfordringer i øjeblikket', 'info')

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
    return render_template('challenges.html')
