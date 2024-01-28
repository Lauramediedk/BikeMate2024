from flask import Blueprint
from .views import signup  # noqa

users_bp = Blueprint('users', __name__)
