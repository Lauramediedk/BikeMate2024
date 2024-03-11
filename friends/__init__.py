from flask import Blueprint

friends_bp = Blueprint('friends', __name__)

from .views import * # noqa