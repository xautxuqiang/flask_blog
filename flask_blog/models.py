from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    head_portrait = db.Column(db.LargeBinary) 
    introduction = db.Column(db.Text)
    posts = db.relationship('Post', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User:{}>'.format(self.username)


tags = db.Table('post_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True)
)


class Post(db.Model):

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    published_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


    def __repr__(self):
        return '<Post:{}>'.format(self.title)


class Tag(db.Model):

    __tablename__ = 'tag'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(255))

    def __repr__(self):
        return '<Tag:{}>'.format(self.tag_name)    

class Category(db.Model):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(255))
    posts = db.relationship('Post', backref="category", lazy="dynamic" )

    def __repr__(self):
        return '{}'.format(self.category_name)

class Comment(db.Model):

    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment:{}>'.format(self.username)

