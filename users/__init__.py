from flask import Blueprint

users_bp = Blueprint('users', __name__)

from .views import signup as _ #  We use _ to avoid linting errors for un-used imports