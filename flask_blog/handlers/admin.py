from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, login_user, logout_user
from flask_blog.forms import LoginForm, UserCreateForm, CategoryCreateForm, TagCreateForm, UserEditForm, CategoryEditForm, TagEditForm, PostCreateForm
from flask_blog.models import User, Post, Category, Tag, db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
@login_required
def index():
    return render_template('admin/index.html')

@admin.route('/user')
@login_required
def admin_user():
    page = request.args.get('page', default=1, type=int)
    pagination = User.query.order_by('id').paginate(
        page = page, 
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False,
    ) 
    user_num = User.query.count()
    return render_template('admin/user.html', pagination=pagination, user_num=user_num)

@admin.route('/user/create', methods=['GET', 'POST'])
@login_required
def admin_user_create():
    form = UserCreateForm()
    if form.validate_on_submit():
        form.create_user()
        flash(u"创建用户成功", 'success')
        return redirect(url_for('admin.admin_user'))
    return render_template('admin/userCreate.html', form=form)

@admin.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        print(user.username)
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash(u"用户名已经存在", 'warning')
        else:
            flash(u'用户更新成功', 'success')
            return redirect(url_for('admin.admin_user'))
    return render_template('admin/userEdit.html', form=form, user=user)
        
    

@admin.route('/user/<int:user_id>/delete')
@login_required
def admin_user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if user.username == 'admin':
        flash(u"admin用户不能被删除", 'danger')
    else:
        db.session.delete(user)
        db.session.commit()
        flash(u"删除该用户成功", 'success')
    return redirect(url_for('admin.admin_user'))
    
@admin.route('/post')
@login_required
def admin_post():
    page = request.args.get('page', default=1, type=int)
    pagination = Post.query.order_by('id').paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False,
    )
    post_num = Post.query.count()
    return render_template('admin/post.html', pagination=pagination, post_num=post_num)

tags_list = []

@admin.route('/post/create', methods=['GET', 'POST'])
@login_required
def admin_post_create():
    form = PostCreateForm()
    tags = Tag.query.all()
    #从js中的url取出标签列表
    ttags = request.args.get('ttags')
    #如果范围的ttags不为空，则如下。应为post两次网址，就第一次会从url中返回，第二次返回为None。可能是应为ajax请求的原因。
    global tags_list
    if ttags:
        tags_list = ttags.split(',')
        #print(tags_list)
    form.user.choices = [(user.id, user.username) for user in User.query.all()]
    form.category.choices = [(category.id, category.category_name) for category in Category.query.all()]
  
    edit = False

    if form.validate_on_submit():
        if tags_list:
            post = Post()
            post.title = form.title.data
            post.content = form.content.data
            post.published_date = form.published_date.data
            post.user_id = form.user.data
            post.category_id = form.category.data
            for tag in tags_list:
                post.tags.append(Tag.query.filter_by(tag_name=tag).first()) 
            db.session.add(post)
            try:
                db.session.commit()
            except Exception:
                flash(u"添加博客失败", 'warning')
                db.session.rollback() 
                tags_list = []
            else:
                flash(u"添加博客成功", 'success')
                tags_list = []
                return redirect(url_for('admin.admin_post'))
        else:
            flash(u"请选择相应标签，如果没有可创建标签", 'warning')
    return render_template('admin/postCreate.html', form=form, tags=tags, edit=edit)

@admin.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    form = PostCreateForm(obj=post)
    form.user.choices = [(user.id, user.username) for user in User.query.all()]
    form.category.choices = [(category.id, category.category_name) for category in Category.query.all()]

    ttags = request.args.get('ttags')
    global tags_list
    if ttags:
        tags_list = ttags.split(',')

    #判断视图为修改，让button显示为更新
    edit = True

    if form.validate_on_submit():
        if tags_list:
            post.title = form.title.data
            post.content = form.content.data
            post.published_date = form.published_date.data
            post.user_id = form.user.data
            post.category_id = form.category.data
            post.tags = []
            for tag in tags_list:
                post.tags.append(Tag.query.filter_by(tag_name=tag).first())
            db.session.add(post)
            try:
                db.session.commit()
            except Exception:
                flash(u"更新博客失败", 'warning')
                db.session.rollback()
                tags_list = []
            else:
                flash(u"更新博客成功", 'success')
                tags_list = []
                return redirect(url_for('admin.admin_post'))
        else:
            flash(u"请选择相应标签，如果没有可创建标签", 'warning')
    return render_template('admin/postEdit.html', form=form, post=post, tags=tags, edit=edit)

@admin.route('/post/<int:post_id>/delete')
@login_required
def admin_post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(u"删除该博客成功", 'success')
    return redirect(url_for('admin.admin_post'))

@admin.route('/category')
@login_required
def admin_category():
    page = request.args.get('page', default=1, type=int)
    pagination = Category.query.order_by('id').paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False,
    )
    category_num = Category.query.count()
    return render_template('admin/category.html', pagination=pagination, category_num=category_num)

@admin.route('/category/create', methods=['GET', 'POST'])
@login_required
def admin_category_create():
    form = CategoryCreateForm()
    if form.validate_on_submit():
        form.create_category()
        flash(u'创建该类别成功', 'success')
        return redirect(url_for('admin.admin_category'))
    return render_template('admin/categoryCreate.html', form=form)

@admin.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_category_edit(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryEditForm(obj=category)
    if form.validate_on_submit():
        category.category_name = form.category_name.data
        db.session.add(category)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash(u"该类别名已经存在",'warning')
        else:
            flash(u"更新该类别成功",'success')
            return redirect(url_for('admin.admin_category'))
    return render_template('admin/categoryEdit.html', form=form, category=category)

    

@admin.route('/category/<int:category_id>/delete')
@login_required
def admin_category_delete(category_id):
    category = Category.query.get_or_404(category_id)
    if Post.query.filter_by(category_id=category_id).count():
        flash(u"该类别对应有相关的博客文章",'warning')
    else:
        db.session.delete(category)  
        db.session.commit()
        flash(u"删除该类别成功", 'success')
    return redirect(url_for('admin.admin_category'))

@admin.route('/tag')
@login_required
def admin_tag():
    page = request.args.get('page', default=1, type=int)
    pagination = Tag.query.order_by('id').paginate(
        page = page,
        per_page = current_app.config['ADMIN_PER_PAGE'],
        error_out = False,
    )
    tag_num = Tag.query.count()
    return render_template('admin/tag.html', pagination=pagination, tag_num=tag_num)

@admin.route('/tag/create', methods=['GET', 'POST'])
@login_required
def admin_tag_create():
    form = TagCreateForm()
    if form.validate_on_submit():
        form.create_tag()
        flash(u"创建该标签成功", 'success')
        return redirect(url_for("admin.admin_tag"))
    return render_template('admin/tagCreate.html', form=form)

@admin.route('/tag/<int:tag_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_tag_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    form = TagEditForm(obj=tag)
    if form.validate_on_submit():
        tag.tag_name = form.tag_name.data
        db.session.add(tag)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash(u"该标签已经存在", 'warning')
        else:
            flash(u"更新该标签成功", 'success')
            return redirect(url_for('admin.admin_tag'))
    return render_template('admin/tagEdit.html', form=form, tag=tag)

@admin.route('/tag/<int:tag_id>/delete')
@login_required
def admin_tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    if tag.posts.count():
        flash(u"该标签对应有相关的博客", 'warning')
    else:
        db.session.delete(tag)
        db.session.commit()
        flash(u"删除该标签成功", 'success')
    return redirect(url_for('admin.admin_tag'))


@admin.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, form.remember_me.data)
        flash(u'登陆成功', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/login.html', form=form)

@admin.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'注销成功', 'success')
    return redirect(url_for('admin.login'))
