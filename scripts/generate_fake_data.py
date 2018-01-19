from faker import Faker
from datetime import datetime
from flask_blog.models import db, Post, Category
import random

fake = Faker('zh-CN')

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
        )

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
