from flask import render_template, request, redirect, url_for, flash, abort, session
from app import db
from app.posts import post_bp
from app.posts.models import Post
from app.posts.forms import PostForm

@post_bp.route('/', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.posted.desc()).all()
    return render_template('posts/posts.html', posts=posts)

@post_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
         
        author_name = session.get('username', 'Anonymous')
        
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            author=author_name
        )
        db.session.add(new_post)
        db.session.commit()
        
        flash("Post added successfully", "success")
        return redirect(url_for('posts.get_posts'))
        
    return render_template('posts/add_post.html', form=form)

 
@post_bp.route('/<int:id>', methods=['GET'])
def detail_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template('posts/detail_post.html', post=post)

 
@post_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
        
    form = PostForm(obj=post)
    
    if request.method == 'GET':
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
         
        post.posted = form.publish_date.data
        db.session.commit()
        
        flash("Пост оновлено!", "success")
        return redirect(url_for('posts.detail_post', id=post.id))
        
    return render_template('posts/add_post.html', form=form, title="Редагувати пост")

 
@post_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
        
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for('posts.get_posts'))
        
    return render_template('posts/delete_confirm.html', post=post)