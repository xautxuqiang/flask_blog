from faker import Faker
from datetime import datetime
from flask_blog.models import db, Post, Category, User, Tag
import random

fake = Faker('zh-CN')

tag_list = []

def iter_category():
   category_list = ['python','django','flask','数据结构','心得感悟','linux','docker','数据库','前端开发','后端开发']
   for i in range(10):
       yield Category (
           category_name = category_list[i]
       )

def iter_post():
    for i in range(100):
        yield Post(
            title = fake.sentence(),
            content = fake.text(),
            published_date = datetime.utcnow(),
            user_id = 1,
            category_id = random.randint(1,10),
            tags = random.sample(tag_list, 2),
        )

def run_user():
    user = User(username='admin', password='xqxq1994')
    db.session.add(user)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()

def run_category():
    for category in iter_category():
        db.session.add(category)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def run_post():
    for post in iter_post():
        db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()


def iter_tag():
    for tmp in ["Python", "微信公众平台开发", "微信支付", "MD5", "UUID", "二叉树", "迭代器", "REST", "服务器部署", "线程"]:
        tag = Tag(tag_name=tmp)
        tag_list.append(tag)
        yield tag

def run_tag():
    for tag in iter_tag():
        db.session.add(tag)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()    

def run():
    run_user()
    run_category()
    run_tag()
    run_post()
