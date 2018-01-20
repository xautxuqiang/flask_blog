from flask import Blueprint, render_template, current_app, request
from flask_blog.models import Post, Category


blog = Blueprint('blog', __name__, url_prefix='/blog')

@blog.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    category_id = request.args.get('cat')
    if category_id:
        pagination = Post.query.filter_by(category_id=category_id).paginate(
            page = page,
            per_page = current_app.config['BLOG_PER_PAGE'],
            error_out = False
        )
    else:
        pagination = Post.query.paginate(
            page = page,
            per_page = current_app.config['BLOG_PER_PAGE'],
            error_out = False
        )

    category_list_and_num = []
    category_list = Category.query.all()
    for category in category_list:
        num = Post.query.filter_by(category_id=category.id).count()
        category_list_and_num.append([category, num])
    return render_template('blog.html', pagination=pagination, category_id=category_id, category_list_and_num=category_list_and_num)


@blog.route('/<int:post_id>')
def the_post(post_id):
    post = Post.query.filter_by(id=post_id).first()

    category_list_and_num = []
    category_list = Category.query.all()
    for category in category_list:
        num = Post.query.filter_by(category_id=category.id).count()
        category_list_and_num.append([category, num])

    return render_template('post.html', post=post, category_list_and_num=category_list_and_num)
