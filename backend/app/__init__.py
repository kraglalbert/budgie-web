import os

from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPTokenAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

from config import config

db = SQLAlchemy()
migrate = Migrate()
http_auth = HTTPTokenAuth("Bearer")


def create_app(config_name):
    app = Flask(__name__)
    CORS(
        app,
        resources={
            r"/*": {"origins": [r"http://localhost:*", r"http://192.168.0.11:*"]}
        },
    )
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG" or "default")

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # call init_app to complete initialization
    db.init_app(app)
    migrate.init_app(app, db)

    # create app blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .categories import categories as categories_blueprint

    app.register_blueprint(categories_blueprint, url_prefix="/categories")

    from .users import users as users_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/users")

    from .transactions import transactions as transactions_blueprint

    app.register_blueprint(transactions_blueprint, url_prefix="/transactions")

    return app
