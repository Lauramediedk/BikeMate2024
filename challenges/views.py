from flask import render_template, flash, session, request, redirect, url_for
from . import challenges_bp
from .forms import EventForm
from .models import Events
from users.views import login_required

@challenges_bp.route('/')
@login_required
def challenges():
    user_id = session.get('user_id')

    form = EventForm()

    if 'user_id' in session:
        return render_template('challenges.html', form=form, active_page='challenges')
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
