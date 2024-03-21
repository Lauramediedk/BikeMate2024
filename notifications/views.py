from flask import session, render_template, flash, redirect, url_for, request
from . import notif_bp
from .models import get_user_invites
from friends.models import get_friend_requests, accept_friend_request, delete_friend_request


@notif_bp.route('/handle_friend_request/<action>/<from_user_id>', methods=['POST'])
def handle_friend_request(action, from_user_id):
    to_user_id = session.get('user_id')
    if action == 'accept':
        if accept_friend_request(from_user_id, to_user_id):
            flash('Tilføjet til venner', 'success')
        else:
            flash('Kunne ikke acceptere anmodning, prøv igen', 'error')
    elif action == 'delete':
        if delete_friend_request(from_user_id, to_user_id):
            flash('Anmodning slettet', 'success')
        else:
            flash('Kunne ikke slette anmodningen, prøv igen', 'error')
    return redirect(request.referrer or url_for('dashboard.dashboard'))
    # Redirect to the current page or the dashboard as a fallback


@notif_bp.route('/update_list')
def update_notifications():
    user_id = session.get('user_id')
    invitations = get_user_invites(user_id)
    friend_requests = get_friend_requests(user_id)
    new_notifications = len(invitations) > 0 # Check if there is any
    session['new_notifications'] = new_notifications # Save it in session to use all places
    # Render only the notification list part of the template
    return render_template('notif_list.html', invitations=invitations, friend_requests=friend_requests)
