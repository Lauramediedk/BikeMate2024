from flask import render_template, session, flash, url_for, redirect, request
from . import friends_bp
from users.views import login_required
from .models import send_friend_request, search_user

@friends_bp.route('/')
@login_required
def friends():
    search_term = request.args.get('search_term', '')
    results = []

    if search_term:
        results = search_user(search_term)
        if not results:
            flash('Kunne ikke finde nogle brugere med det navn', 'error')

    return render_template('friends.html',
                           search_term=search_term,
                           results=results,
                           active_page='friends')

@friends_bp.route('/send_request/<to_user_id>', methods=['POST'])
@login_required
def send_request(to_user_id):
    from_user_id = session.get('user_id')

    if send_friend_request(from_user_id, to_user_id):
        flash('Anmodning sendt til brugeren', 'success')
    else:
        flash('Anmodningen kunne ikke sendes, prøv igen', 'error')
    return redirect(url_for('friends.friends'))
