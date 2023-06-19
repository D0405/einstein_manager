from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import json

from sqlalchemy.ext.declarative import DeclarativeMeta

db = SQLAlchemy()
DB_NAME = "database.db"

import json
from sqlalchemy.ext.declarative import DeclarativeMeta

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
        return super().default(obj)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'devremoveaftdderdeployAndFix'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.json_encoder = CustomJSONEncoder
    db.init_app(app)





    #Use blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))



    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created Database!")


