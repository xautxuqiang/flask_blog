from flask import Blueprint, render_template, current_app, request
from flask_blog.models import Post, Category


blog = Blueprint('blog', __name__, url_prefix='/blog')

@blog.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Post.query.paginate(
        page = page,
        per_page = current_app.config['BLOG_PER_PAGE'],
        error_out = False
    )
    category_list_and_num = []
    category_list = Category.query.all()
    for category in category_list:
        num = Post.query.filter_by(category_id=category.id).count()
        category_list_and_num.append([category,num])
    return render_template('blog.html', pagination=pagination, category_list_and_num=category_list_and_num)

@blog.route('/category/<int:category_id>')
def category(category_id):
    posts = Post.query.filter_by(category_id=category_id).all()
    category_list_and_num = []
    category_list = Category.query.all()
    for category in category_list:
        num = Post.query.filter_by(category_id=category.id).count()
        category_list_and_num.append([category.category_name,num])
    return render_template('blog_category.html', posts=posts, category_list_and_num=category_list_and_num)
