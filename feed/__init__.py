from flask import Blueprint

feed_bp = Blueprint('feed', __name__)

from .views import feed, delete_post  # noqa