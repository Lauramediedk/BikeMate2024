from flask import Blueprint

notif_bp = Blueprint('notifications', __name__)

from .views import * # noqa