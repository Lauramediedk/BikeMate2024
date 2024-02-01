from . import feed_bp
from flask import render_template, session, redirect, flash, url_for
from users.views import login_required
from .forms import PostForm
from .models import Post

@feed_bp.route('/', methods=['GET', 'POST'])
@login_required
def feed():
    form = PostForm()
    user_id = session.get('user_id')
    if form.validate_on_submit():
        try:
            post = Post(
                content=form.content.data,
                image_path=form.image_path.data,
                is_private=form.is_private.data,
                author=user_id
            )
            post.create_post()

            flash('Opslag oprettet', 'success')
            return redirect(url_for('feed.feed'))
        except Exception as e:
            flash(f"Error occured during creation of post: {str(e)}", 'error')

    return render_template('feed.html', form=form, active_page='feed')
