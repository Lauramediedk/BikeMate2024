from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from .views import dashboard, upload_picture, remove_picture, upload_user_bio, get_user_bio, logout  # noqa
