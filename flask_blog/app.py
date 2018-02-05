from flask import Flask
from flask_blog.config import configs
from flask_blog.models import db, User
from flask_blog.handlers import front, blog, admin, live
from flask_migrate import Migrate
from flask_login import LoginManager

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    login_manager.login_view = 'admin.login'
    login_manager.session_protection = "strong"
    login_manager.login_message = u"进入管理页面前请登录"
    login_manager.login_message_category = "info"

def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(blog)
    app.register_blueprint(admin)
    app.register_blueprint(live)
