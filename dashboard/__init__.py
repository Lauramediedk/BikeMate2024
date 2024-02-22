from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from .views import dashboard, upload_picture, remove_picture, upload_bio, logout  # noqa
