from flask import Blueprint

challenges_bp = Blueprint('challenges', __name__)

from .views import challenges, show_event_form, create_event, users_events, all_events # noqa