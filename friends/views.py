from flask import render_template, session, flash, url_for, redirect, request
from . import friends_bp
from users.views import login_required
from .models import send_friend_request, search_user, get_friend_requests, accept_friend_request, delete_friend_request, check_friendship, get_recommended_friends, delete_friendship, view_profile


@friends_bp.route('/')
@login_required
def friends():
    search_term = request.args.get('search_term', '')
    user_id = session.get('user_id')
    friend_requests = get_friend_requests(user_id)
    recommended_friends = get_recommended_friends(user_id)
    results = []

    if search_term:
        results = search_user(search_term, user_id)
        if not results:
            flash('Kunne ikke finde nogle brugere med det navn', 'error')

    return render_template('friends.html',
                           search_term=search_term,
                           friend_requests=friend_requests,
                           results=results,
                           recommended_friends=recommended_friends,
                           active_page='friends')


@friends_bp.route('/profile/<string:user_id>', methods=['GET'])
@login_required
def profile(user_id):
    logged_in_user = session.get('user_id')

    profile = view_profile(user_id, logged_in_user)
    if profile:
        return render_template('public_dashboard.html', profile=profile, active_page='friends')
    else:
        flash('Brugerens dashboard kunne ikke tilgås, prøv igen', 'error')
        return redirect(url_for('friends.friends'))


@friends_bp.route('/accept_request/<from_user_id>', methods=['POST'])
@login_required
def accept_request(from_user_id):
    to_user_id = session.get('user_id')

    if accept_friend_request(from_user_id, to_user_id):
        flash('Tilføjet til venner', 'success')
    else:
        flash('Kunne ikke tilføje bruger som ven, prøv igen', 'error')
    return redirect(url_for('friends.friends'))


@friends_bp.route('/delete_request/<from_user_id>', methods=['POST'])
@login_required
def delete_request(from_user_id):
    to_user_id = session.get('user_id')

    if delete_friend_request(from_user_id, to_user_id):
        flash('Venne anmodning slettet', 'success')
    else:
        flash('Anmodningen kunne ikke slettes, prøv igen', 'error')
    return redirect(url_for('friends.friends'))


@friends_bp.route('/toggle_friendship/<to_user_id>', methods=['POST'])
@login_required
def toggle_friendship(to_user_id):
    from_user_id = session.get('user_id')

    if check_friendship(from_user_id, to_user_id):
        if delete_friendship(from_user_id, to_user_id):
            flash('Fjernet fra venner', 'success')
        else:
            flash('Kunne ikke fjerne fra venner, prøv igen', 'error')
    else:
        if send_friend_request(from_user_id, to_user_id):
            flash('Anmodning sendt til brugeren', 'success')
        else:
            flash('Anmodningen kunne ikke sendes, prøv igen', 'error')

    return redirect(url_for('friends.friends'))
