from apiflask import APIFlask
from flask_sqlalchemy import SQLAlchemy

from apis.auth import auth
from apis.restaurants import restaurants
from config import flask_config

db = SQLAlchemy()


def create_app():
    app = APIFlask(__name__, title="Halal Restaurants Application", version="1.0")
    config = flask_config['development']
    app.config.from_object(config)
    app.logger.setLevel(config.LOGGING_LEVEL_MAPPED)
    db.init_app(app)

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(restaurants, url_prefix="/restaurants")

    return app
