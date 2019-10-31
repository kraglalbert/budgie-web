from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # call init_app to complete initialization
    db.init_app(app)
    login_manager.init_app(app)

    # create app blueprints
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint

    app.register_blueprint(account_blueprint, url_prefix="/account")

    from .users import users as users_blueprint

    app.register_blueprint(users_blueprint, url_prefix="/users")

    from .transactions import transactions as transactions_blueprint

    app.register_blueprint(transactions_blueprint, url_prefix="/transactions")

    return app
