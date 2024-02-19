from flask import render_template, flash, redirect, url_for, session, request
from config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename
from . import dashboard_bp
from .forms import BioForm
from users.views import login_required
from .models import upload_profile_image, get_profile_image, remove_profile_image, upload_user_bio, get_user_bio
import os


@dashboard_bp.route('/')
@login_required
def dashboard():
    user_id = session.get('user_id')
    first_name = session.get('first_name')
    last_name = session.get('last_name')
    image_path = get_profile_image(user_id)
    bio = get_user_bio(user_id)

    form = BioForm()

    if 'user_id' in session:
        return render_template('dashboard.html', first_name=first_name, last_name=last_name, image_path=image_path, bio=bio, form=form, active_page='dashboard')
    else:
        flash('Adgang nægtet', 'error')
    return redirect(url_for('users.login'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@dashboard_bp.route('/upload_picture', methods=['POST'])
def upload_picture():
    if 'file' not in request.files:
        flash('Ingen fil', 'error')
        return redirect(url_for('dashboard.dashboard'))

    file = request.files['file']
    if file.filename == '':
        flash('Ingen fil valgt', 'error')
        return redirect(url_for('dashboard.dashboard'))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        user_id = session.get('user_id')
        upload_profile_image(user_id, f'/uploads/{filename}')

        flash('Billede uploadet succesfuldt', 'success')
    else:
        flash('Ugyldigt filformat', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/remove_picture', methods=['GET', 'POST'])
def remove_picture():
    try:
        user_id = session.get('user_id')
        image_path = get_profile_image(user_id)

        if image_path:
            remove_profile_image(user_id)
            file = os.path.join(UPLOAD_FOLDER, os.path.basename(image_path))

            if os.path.exists(file):
                os.remove(file)

            flash('Billede fjernet', 'success')
        else:
            flash('Intet profilbillede at fjerne', 'error')
    except Exception as e:
        flash(f'Kunne ikke fjerne billedet: {str(e)}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/upload_bio', methods=['POST'])
def upload_bio():
    user_id = session.get('user_id')
    form = BioForm()

    if form.validate_on_submit():
        new_bio = form.description.data
        try:
            upload_user_bio(user_id, new_bio)
            flash('Bio opdateret', 'success')
        except Exception as e:
            flash(f'Kunne ikke fjerne billedet: {str(e)}', 'error')

    return redirect(url_for('dashboard.dashboard'))


@dashboard_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('first_name', None)
    session.pop('last_name', None)

    return redirect(url_for('dashboard.dashboard'))
