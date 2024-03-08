from flask import render_template, flash, session, request, redirect, url_for
from . import challenges_bp
from .forms import EventForm
from .models import Events
from users.views import login_required


def format_date(events):
    for event in events:
        event.created_formatted = event.date.strftime('%d. %m. %Y')


@challenges_bp.route('/', methods=['GET', 'POST'])
@login_required
def challenges():
    user_id = session.get('user_id')

    search_term = request.args.get('search_term', '')
    popular = request.args.get('popular', False)

    form = EventForm()
    if search_term:
        all_events = Events.search_for_event(user_id, search_term)
    elif popular:
        all_events = Events.get_popular_events(user_id)
    else:
        all_events = Events.get_all_events(user_id)

    users_events = Events.get_own_events(user_id)

    format_date(all_events)
    format_date(users_events)

    if 'user_id' in session:
        return render_template('challenges.html',
        form=form,
        all_events=all_events,
        users_events=users_events,
        search_term=search_term,
        popular=popular,
        active_page='challenges')
    else:
        flash('Adgang nægtet', 'error')
        return redirect(url_for('users.login'))


@challenges_bp.route('/create_event', methods=['GET'])
@login_required
def show_event_form():
    form = EventForm()
    return render_template('create_event.html', form=form, active_page='challenges')


@challenges_bp.route('/create_event', methods=['POST'])
@login_required
def create_event():
    user_id = session.get('user_id')
    form = EventForm()

    if form.validate_on_submit():
        event = Events(
            title=form.title.data,
            description=form.description.data,
            date=form.startdate.data,
            location=form.location.data,
            admin=user_id
        )
        event.create_event(user_id=user_id)
        flash('Event oprettet', 'success')

        return redirect(url_for('challenges.challenges'))

    else:
        flash('Kunne ikke oprette event', 'error')

    return render_template('create_event.html', form=form)


@challenges_bp.route('/delete/<event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    user_id = session.get('user_id')

    if user_id:
        if event_id:
            Events.delete_event(user_id, event_id)
            flash('Du har slettet et event', 'success')
            return redirect(url_for('challenges.challenges'))
        else:
            flash('Event kunne ikke slettes, prøv igen', 'error')
    else:
        flash('Uautoriseret adgang', 'error')

    return redirect(url_for('challenges.view_event', event_id=event_id))


@challenges_bp.route('/event/<event_id>', methods=['GET'])
@login_required
def view_event(event_id):
    user_id = session.get('user_id')

    # Get event details by event_id
    event = Events.get_event_by_id(event_id)
    is_joined = Events.is_user_joined(user_id, event_id)
    participants = Events.get_participants(event_id)

    if event:
        return render_template('view_event.html',
        is_joined=is_joined,
        event=event,
        participants=participants,
        active_page='challenges')
    else:
        flash('Event ikke fundet', 'error')
        return redirect(url_for('challenges.challenges'))


@challenges_bp.route('/join/<event_id>', methods=['POST'])
@login_required
def join_event(event_id):
    user_id = session.get('user_id')

    if event_id:
        Events.join_event(user_id, event_id)
        flash('Du deltager nu i dette event.', 'success')
    else:
        flash('Event id kunne ikke tilgås', 'error')

    return redirect(url_for('challenges.view_event', event_id=event_id))


@challenges_bp.route('/unjoin_event/<event_id>', methods=['POST'])
@login_required
def unjoin_event(event_id):
    user_id = session.get('user_id')

    Events.unjoin_event(user_id, event_id)
    flash('Du deltager ikke længere i dette event', 'success')

    return redirect(url_for('challenges.challenges', event_id=event_id))