from flask import Flask
from flask_blog.config import configs
from flask_blog.models import db
from flask_blog.handlers import front, blog, admin
from flask_migrate import Migrate

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)
    

def register_blueprints(app):
    app.register_blueprint(front)
    app.register_blueprint(blog)
    app.register_blueprint(admin)
