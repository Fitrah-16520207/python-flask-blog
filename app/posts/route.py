from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from app import db
from app.model import Post
from app.posts.forms import PostForm
from flask_login import current_user, login_required


posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET','POST'])
@login_required
def post_baru():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post Anda telah dibuat!','success')
        return redirect(url_for('main.rumah'))
    return render_template('create_post.html',title = 'Buat Post', form=form, legend='Buat Post')

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Anda telah diperbarui!",'success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET' :
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html',title = 'Perbarui Post', form=form, legend='Perbarui Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def hapus_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Anda telah dihapus!",'success')
    return redirect(url_for('main.rumah'))


