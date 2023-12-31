from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from gitsummary.config import Config




db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'alert alert-info'

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from gitsummary.users.routes import users
    from gitsummary.repos.routes import repos
    from gitsummary.main.routes import main
    from gitsummary.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(repos)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app