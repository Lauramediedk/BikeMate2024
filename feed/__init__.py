from flask import Blueprint

feed_bp = Blueprint('feed', __name__)

from .views import feed, edit_post, delete_post  # noqa