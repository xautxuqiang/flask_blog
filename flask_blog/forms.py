from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, DateTimeField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from flask_blog.models import User, db, Category, Tag
from datetime import datetime


class LoginForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(message=u"该字段不能为空"), Length(1,255, message="用户名的长度超出范围")])
    password = PasswordField(u'密码', validators=[DataRequired(message=u"该字段不能为空"), Length(6,24, message=u"密码长度位于6到24之间")])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField('登录')

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('无效的用户名')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('密码错误')
            return False

        return True 

class UserCreateForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度不超过255")])
    password = PasswordField(u'密码', validators=[DataRequired(u'该字段不能为空'), Length(6, 24, message=u"密码长度位于6到24位之间")])
    submit = SubmitField(u"创建")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u"该用户已经存在")

    def create_user(self):
        user = User()
        user.username = self.username.data
        user.password = self.password.data
        db.session.add(user)
        db.session.commit()
        return user

class UserEditForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度不超过255")])
    password = PasswordField(u'密码', validators=[DataRequired(u'该字段不能为空'), Length(6, 24, message=u"密码长度位于6到24位之间")])
    submit = SubmitField(u"更新")


class CategoryCreateForm(FlaskForm):
    category_name = StringField(u'类别名', validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度不超过255")])
    submit = SubmitField(u"创建")

    def validate_category_name(self, field):
        if Category.query.filter_by(category_name=field.data).first():
           raise ValidationError(u"该类别已经存在")

    def create_category(self):
        category = Category()
        category.category_name = self.category_name.data
        db.session.add(category)
        db.session.commit()
        return category

class CategoryEditForm(FlaskForm):
    category_name = StringField(u'类别名', validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度小于255")])
    submit = SubmitField(u"更新")


class TagCreateForm(FlaskForm):
    tag_name = StringField(u"标签名", validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度小于255")])
    submit = SubmitField(u"创建")

    def validate_tag_name(self, field):
        if Tag.query.filter_by(tag_name=field.data).first():
            raise ValidationError(u"该标签已经存在")

    def create_tag(self):
        tag = Tag()
        tag.tag_name = self.tag_name.data
        db.session.add(tag)
        db.session.commit()
        return tag

class TagEditForm(FlaskForm):
    tag_name = StringField(u"标签名", validators=[DataRequired(u'该字段不能为空'), Length(1,255, message=u"该字段长度不超过255")])
    submit = SubmitField(u"更新")

class PostCreateForm(FlaskForm):
    title = StringField(u"标题", validators=[DataRequired(u"该字段不能为空"), Length(1,255 ,message=u"该字段长度不超过255")])
    content = TextAreaField(u"内容")
    published_date = DateTimeField(u"创建时间", default=datetime.utcnow()) 
    user = SelectField(u'用户', coerce=int)
    category = SelectField(u"类别", coerce=int)
