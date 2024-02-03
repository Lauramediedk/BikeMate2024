from . import feed_bp
from flask import render_template, session, redirect, flash, url_for, request
from users.views import login_required
from .forms import PostForm
from .models import Post

@feed_bp.route('/', methods=['GET', 'POST'])
@login_required
def feed():
    form = PostForm()

    try:
        if request.method == 'POST':

            if form.validate_on_submit():
                user_id = session.get('user_id')
                first_name = session.get('first_name')
                post = Post(
                    content=form.content.data,
                    image_path=form.image_path.data,
                    is_private=form.is_private.data,
                    author_id=user_id,
                    author_name=first_name
                )
                post.create_post()

                flash('Opslag oprettet', 'success')
                return redirect(url_for('feed.feed'))

        else:
            search_content = request.args.get('search_content')

            if search_content:
                posts = Post.search_post(search_content)
                return render_template('feed.html', posts=posts, form=form, active_page='feed')
            else:
                posts = Post.get_posts()

            if posts:
                return render_template('feed.html', posts=posts, form=form, active_page='feed')

            else:
                flash('Ingen opslag i øjeblikket', 'info')

    except Exception as e:
        flash(f"Error occured during creation of post: {str(e)}", 'error')

    return render_template('feed.html', form=form, active_page='feed')


@feed_bp.route('/feed/<string:post_id>', methods=['POST'])
@login_required
def edit_post(post_id):
    user_id = session.get('user_id')
    new_content = request.form.get('new_content')

    try:
        Post.edit_post(post_id, user_id, new_content)
        flash('Opslag ændret', 'success')

    except Exception as e:
        flash(f"Fejl. Kunne ikke ændre opslag: {str(e)}", 'error')

    return redirect(url_for('feed.feed'))


@feed_bp.route('/feed/delete/<string:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    user_id = session.get('user_id')

    try:
        Post.delete_post(post_id, user_id)
        flash('Opslag slettet', 'success')

    except Exception as e:
        flash(f"Error occurred during deletion of post: {str(e)}", 'error')

    return redirect(url_for('feed.feed'))
